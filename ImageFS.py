#!/usr/bin/python

from fuse import Fuse

from time import time

import stat    # for file properties
import os      # for filesystem modes (O_RDONLY, etc)
import errno   # for error number codes (ENOENT, etc)
               # - note: these must be returned as negatives

import json
import flickrapi



def dirFromList(list):
    """
    Return a properly formatted list of items suitable to a directory listing.
    ['a',_'b',_'c'] =&gt; [('a',_0),_('b',_0),_('c',_0)]
    """
    return [(x,_0)_for_x_in_list]

def getDepth(path):
    """
    Return the depth of a given path, zero-based from root ('/')
    """
    if path == '/':
       return 0
    else:
       return path.count('/')

def getParts(path):

    """
    Return the slash-separated parts of a given path as a list
    """

    if path == '/':
       return ['/']
    else:
       return path.split('/')

class ImageFS(Fuse):

   """
   """

   def __init__(self, *args, **kw):
       Fuse.__init__(self, *args, **kw)

       flickr_api_key = u'XXX'
       flickr_api_secret = u'XXX'
       self.flickr = flickrapi.FlickrAPI(flickr_api_key, flickr_api_secret, format='json')

       print 'Init complete.'

  def getattr(self, path):
    st = MyStat()
    pe = path.split('/')[1:]

    st.st_atime = int(time())
    st.st_mtime = st.st_atime
    st.st_ctime = st.st_atime

    if path == '/':                         # root
        pass
    elif self.printers.has_key(pe[-1]):     # a printer
        pass
    elif self.lastfiles.has_key(pe[-1]):    # a file
        st.st_mode = stat.S_IFREG | 0666
        st.st_nlink = 1
        st.st_size = len(self.lastfiles[pe[-1]]
    else:
        return -errno.ENOENT
    return st


       """
       - st_mode (protection bits)
       - st_ino (inode number)
       - st_dev (device)
       - st_nlink (number of hard links)
       - st_uid (user ID of owner)
       - st_gid (group ID of owner)
       - st_size (size of file, in bytes)
       - st_atime (time of most recent access)
       - st_mtime (time of most recent content modification)
       - st_ctime (platform dependent; time of most recent metadata change on Unix,
                   or the time of creation on Windows).
       """

       print '*** getattr', path

       st = MyStat()
       pe = path.split('/')[1:]

       st.st_atime = int(time())
       st.st_mtime = st.st_atime
       st.st_ctime = st.st_atime

       depth = getDepth(path) # depth of path, zero-based from root
       pathparts = getParts(path) # the actual parts of the path

       return st

   ### HEY KEVIN DO THIS
   ### It's called readdir in the tutorial but it's getdir here I guess
  def getdir(self, path):
       """
       return: [('file1',_0),_('file2',_0),_..._]
       """
    dirents = [ '.', '..' ]
    if path == '/':
      dirents.extend(self.printers.keys())
    else:
     # Note use of path[1:] to strip the leading '/'
     # from the path, so we just get the printer name
     dirents.extend(self.printers[path[1:]])
    for r in dirents:
      yield fuse.Direntry(r)

         print '*** getdir', path
         return -errno.ENOSYS

   def mythread ( self ):
       print '*** mythread'
       return -errno.ENOSYS

   def chmod ( self, path, mode ):
       print '*** chmod', path, oct(mode)
       return -errno.ENOSYS

   def chown ( self, path, uid, gid ):
       print '*** chown', path, uid, gid
       return -errno.ENOSYS

   def fsync ( self, path, isFsyncFile ):
       print '*** fsync', path, isFsyncFile
       return -errno.ENOSYS

   def link ( self, targetPath, linkPath ):
       print '*** link', targetPath, linkPath
       return -errno.ENOSYS

   def mkdir ( self, path, mode ):
       print '*** mkdir', path, oct(mode)
       return -errno.ENOSYS

   def mknod ( self, path, mode, dev ):
       print '*** mknod', path, oct(mode), dev
       return -errno.ENOSYS

   def open ( self, path, flags ):
       print '*** open', path, flags
       return -errno.ENOSYS

   def read ( self, path, length, offset ):
       print '*** read', path, length, offset
       return -errno.ENOSYS

   def readlink ( self, path ):
       print '*** readlink', path
       return -errno.ENOSYS

   def release ( self, path, flags ):
       print '*** release', path, flags
       return -errno.ENOSYS

   def rename ( self, oldPath, newPath ):
       print '*** rename', oldPath, newPath
       return -errno.ENOSYS

   def rmdir ( self, path ):
       print '*** rmdir', path
       return -errno.ENOSYS

   def statfs ( self ):
       print '*** statfs'
       return -errno.ENOSYS

   def symlink ( self, targetPath, linkPath ):
       print '*** symlink', targetPath, linkPath
       return -errno.ENOSYS

   def truncate ( self, path, size ):
       print '*** truncate', path, size
       return -errno.ENOSYS

   def unlink ( self, path ):
       print '*** unlink', path
       return -errno.ENOSYS

   def utime ( self, path, times ):
       print '*** utime', path, times
       return -errno.ENOSYS

   def write ( self, path, buf, offset ):
       print '*** write', path, buf, offset
       return -errno.ENOSYS

# Status object
class MyStat(fuse.Stat):
   def __init__(self):
       self.st_mode = stat.S_IFDIR | 0755
       self.st_ino = 0
       self.st_dev = 0
       self.st_nlink = 2
       self.st_uid = 0
       self.st_gid = 0
       self.st_size = 4096
       self.st_atime = 0
       self.st_mtime = 0
       self.st_ctime = 0

if __name__ == __main__:

    fs = NullFS()
    fs.flags = 0
    fs.multithreaded = 0
    fs.main()