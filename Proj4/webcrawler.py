import requests,re,bs4,matplotlib.pyplot as plt,sys,LinkValidator as lv,image_processing as ip, shutil

def parse_robots(domain_name):
    """Returns the list of paths to exclude from domain_name's robots.txt file."""
    global true_domain
    true_domain="https://"+domain_name.split('/')[2]
    website=requests.get(true_domain+'/robots.txt')
    return re.findall(r"Disallow: (.+)\n",website.text)

def check_command(arguments):
    if len(arguments)==5 and arguments[1] in ['-c','-p','-i']:
        if arguments[1]=="-i":
            if not arguments[4] in ['-s','-g','-f','-m']:
                raise ValueError('You have given invalid arguments')
        return True
    raise ValueError('You have given invalid arguments')

def send_out(args):
    if args[1]=='-c':
        count_links(args[2],args[3],args[4])
    if args[1]=='-p':
        plot_data(args[2],args[3],args[4])
    if args[1]=='-i':
        do_filter(args[2],args[3],args[4])

def get_website(domain):
    web=requests.get(domain)
    soup=bs4.BeautifulSoup(web.content,features='html.parser')
    return soup

def völlständiger(link,url,domain):
    if "#" in link:
        link=link.split("#")[0]
    if link.startswith("/"):
        link=domain+link
    if not link.startswith('https') and not link.startswith('/'):
        end=url.rfind('/')
        link=url[:end]+'/'+link
    return link
        
def count_links(domain,output1,output2):
    
    def count_link_recurse(url):
        website=get_website(url)
        links=website.find_all('a')
        for link in links:
            link=völlständiger(link.get('href'),url,domain)
            if not link in to_visit.keys():
                to_visit[link]=1
                if validator.can_follow_link(link):
                    count_link_recurse(link)
            else:
                to_visit[link]+=1

            
    #Setup
    website=get_website(domain)
    forbidden=parse_robots(domain)
    validator=lv.LinkValidator(true_domain,forbidden)
    to_visit={domain:1}
    #Run
    count_link_recurse(domain)
    #Print Output
    frequencies= [count for count in to_visit.values()]
    plt.hist(frequencies,[1,2,3,4,5,6])
    plt.savefig(output1)
    with open(output2,'w') as f:
        largest=max(sorted(frequencies))
        for num in range(1,largest+1):
            freq=float(num)
            fcount=float(len([item for item in frequencies if item==num]))
            f.write(f'{freq},{fcount}\n')

def plot_data(url,image_out,csv_out):
    try:
        website=get_website(url)
    except Exception as e:
        print("ERROR: ",e)
    #find the right Table
    tables=website.find_all("table")
    real_table=''
    for table in tables:
        if table['id']=="CS111-Project4b":
            real_table=table
            break
    
    # Read through the Table rows
    rows=real_table.find_all('tr')
    list_rows=[]
    for row in rows:
        cells=row.find_all('td')
        list_row=[]
        for cell in cells:
            list_row.append(str(float(cell.get_text())))

        list_rows.append(list_row)

    # Write data to file
    with open(csv_out,'w') as f:
        for row in list_rows:
            f.write(','.join(row)+'\n')
    # Create and Save Plot
    format={1:'b',2:'g',3:'r',4:'k'}
    columns=[[num+1] for num in range(len(list_rows[0]))]
    for row in list_rows:
        for int in range(len(row)):
            columns[int].append(float(row[int]))
    for int in range(len(columns)):
        columns[int]=columns[int][1:]
    for int in range(1,len(columns)):
        plt.plot(columns[0],columns[int],format[int])
    plt.savefig(image_out)

def do_filter(url,prefix,filter):
    try:
        website=get_website(url)
        forbidden=parse_robots(url)
        validator=lv.LinkValidator(true_domain,forbidden)
    except Exception as e:
        print("ERROR: ",e)
    
    #Create a List of all image links on the page
    image_links=[]
    images=website.find_all('img')
    for image in images:
        image=völlständiger(image.get('src'),url,true_domain)
        if validator.can_follow_link(image):
            image_links.append(image)
    # Download all the images to the local disk
    file_names=[]
    for link in image_links:
        output_filename=link.split('/')[len(link.split('/'))-1]
        file_names.append(output_filename)
        response = requests.get(link, stream=True)
        with open(output_filename, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
    #Apply the Filter and Save
    for name in file_names:
        real_output=prefix+name
        if filter=='-s':
            ip.sepia(name,real_output)
        if filter=='-g':
            ip.grayscale(name,real_output)
        if filter=='-f':
            ip.flipped(name,real_output)
        if filter=='-m':
            ip.mirror(name,real_output)

if __name__=="__main__":
    try:
        check_command(sys.argv)
        send_out(sys.argv)
    except ValueError as e:
        print('Error: ',e)