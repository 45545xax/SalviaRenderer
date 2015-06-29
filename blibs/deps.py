﻿import env, urllib2, os, download_list, shutil

def github_commit(commit):
    return "https://raw.githubusercontent.com/wuye9036/SalviaDeps/release/%s/" % commit

CHECK_METHOD_HASH = "CM_HASH"

CHECK_METHOD_TAGF = "CM_TAGF"

RAW_FILE          = "RAW_FILE"
COMPRESSED_FILE   = "CMP_FILE"
COMPRESSED_FOLDER = "CMP_FLDR"

def OS_PATH(p):
    return os.path.join( *p.split('/') )

class download_info(object):
    def __init__(self, source, res_path, check_method, res_type, need_distribute, tag):
        rel_path = OS_PATH(res_path)

        self.source = source
        self.check_method = check_method
        self.tag = tag 
        self.res_type = res_type
        self.store_rel_path = rel_path if self.res_type == RAW_FILE else rel_path + ".7z"
        self.need_distribute = need_distribute
        if self.res_type == RAW_FILE:
            self.dist_rel_path = self.store_rel_path
        elif self.res_type == COMPRESSED_FILE or self.res_type == COMPRESSED_FOLDER:
            self.dist_rel_path = self.relative_path
        else:
            self.dist_rel_path = None

def gen_file_md5(file_name):
    return None

COMMIT = ""

DOWNLOAD_FILE_LIST = [
    download_info(github_commit(COMMIT), res_path, CHECK_METHOD_HASH, res_type, not "7z" in res_path, tag)
    for res_path, res_type, tag in download_list.DOWNLOAD_LIST
    ]

def download_file(url, rel_path):
    u = urllib2.urlopen(url)
    f = open(dest, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    try:
        while True:
            buffer = u.read(block_sz)
            if not buffer: break
            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status,
    except:
        f.close()
    
def extract_zip(file):
    pass
    
def need_update(proj_root, dl_info):
    assert isinstance(dl_info, download_info)
    
    store_path = os.path.join(proj_root, "downloads", dl_info.store_rel_path)
    dist_path  = os.path.join(proj_root, dl_info.dist_rel_path)

    if dl_info.res_type == COMPRESSED_FOLDER:
        if not os.path.isdir(dist_path):
            return True
    else:
        if not os.path.isfile(dist_path):
            return True

    if not os.path.isfile(store_path):
        return True
    
    if gen_file_md5(store_path) != dl_info.tag:
        return True

    return False

def download(proj_root, dl_info):
    pass
    
def distribute(proj_root, dl_info):
    assert isinstance(dl_info, download_info)
    if not dl_info.need_distribute: return
    dist_parent = os.path.dirname(dl_info.dist_rel_path)
    src_full_path = os.path.join(proj_root, "downloads", dl_info.store_rel_path)
    dst_parent_full_path = os.path.join(proj_root, dist_parent)
    if dl_info.res_type in [COMPRESSED_FILE, COMPRESSED_FOLDER]:
        decompress(src_full_path, dst_parent_full_path)
    else:
        shutil.copy(src_full_path, dst_parent_full_path)

def update(proj_root, dl_info):
    if need_update(proj_root, dl_info):
        download(proj_root, dl_info)
        distribute(proj_root, dl_info)