import os

def sources_list(sources, main_condict):
    sources_dict = dict()
    for source in sources:
        if os.path.isfile(main_condict['SourcesPath'][0] + source + '/sources.list'):
            with open(main_condict['SourcesPath'][0] + source + '/sources.list', 'r+') as f:
                sources_dict[source] = list()
                sources_dict[source].append(f.read())
                sources_dict[source].append(0)
    return sources_dict

def sources_delete(source, main_condict):
    if os.path.isfile(main_condict['SourcesPath'][0] + source + '/sources.list'):
        os.remove(main_condict['SourcesPath'][0] + source + '/sources.list')
        os.rmdir(main_condict['SourcesPath'][0] + source)

def sources_modification(source_name, new_sources_content, main_condict):
    try:
        f = open(main_condict['SourcesPath'][0] + source_name + '/sources.list', 'w+')
        f.truncate()
        f.write(new_sources_content)
    except:
        return False
    else:
        return True
