"""
Document this
"""
import sys
import shutil
import subprocess

def tempfolder():
    shutil.copytree('rocknode', '_rocknode')

def create(node):
    # specify hostname
    with open('_rocknode/etc/hostname', 'w') as f:
        f.write('rocknode%d' % node)
    with open('_rocknode/etc/hosts', 'r') as f:
        content = f.read().replace('127.0.1.1 rock64', '127.0.1.1 rocknode%d' % node)
    with open('_rocknode/etc/hosts', 'w') as f:        
        f.write(content)
    
    # set IP address
    with open('_rocknode/etc/dhcpcd.conf', 'r') as f:
        content = f.read().replace('24.9.13.1/24', '24.9.13.%d/24' % node)
    with open('_rocknode/etc/dhcpcd.conf', 'w') as f:
        f.write(content)
    
    # set the elasticsearch node name
    with open('_rocknode/home/rock64/elasticsearch-6.2.4/config/elasticsearch.yml', 'r') as f:
        content = f.read().replace('rocknode-1', 'rocknode-%d' % node)
    with open('_rocknode/home/rock64/elasticsearch-6.2.4/config/elasticsearch.yml', 'w') as f:
        f.write(content)
    
def copy():
    subprocess.run(['cp', '-TRf', '_rocknode/etc/.', '/media/mirko/linux-root/etc'])
    #shutil.copytree('_rocknode/etc', '/media/mirko/linux-root/etc')
    #shutil.copytree('_rocknode/home', '/media/mirko/linux-root/home')

if __name__ == '__main__':
    try:
        action = sys.argv[1]
        node = int(sys.argv[2])
    except:
        sys.exit('sample use: rock.py create 4')
    
    # run
    try:
        if action == 'create':
            tempfolder()
            create(node)
        elif action == 'copy':
            copy()
    except Exception as e:
        print(str(e))
    finally:
        if action == 'copy':
            shutil.rmtree('_rocknode')
        print('Done')
