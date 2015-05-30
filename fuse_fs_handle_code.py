from __future__ import with_statement

import os
import sys
import errno
import json
import itertools

from fuse import FUSE, FuseOSError, Operations
import flickrapi

from subprocess import call, check_output, Popen, PIPE

# Helper to split an iterable (like a buffer) into smaller iterables
# Another version exists using iterators, for greater efficiency, if we need it.
# Code from http://stackoverflow.com/questions/8991506/iterate-an-iterator-by-chunks-of-n-in-python
def grouper(n, iterable):
    it = iter(iterable)
    while True:
       chunk = list(itertools.islice(it, n))
       if not chunk:
           return
       yield chunk


class Passthrough(Operations):
    def __init__(self, root):
        self.root = root
        flickr_key = 'f995167d658b6572aecd4d937b29a656'
        flickr_secret = '5771bf75ffb63f73'

        # Hardcode some temp shit
        self.image_filename = "lena.jpg"

        self.files = {}
        self.devnull = os.open("/dev/null", os.O_RDWR)

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        full_path = self._full_path(path)
        if not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode):
        full_path = self._full_path(path)
        return os.chmod(full_path, mode)

    def chown(self, path, uid, gid):
        full_path = self._full_path(path)
        return os.chown(full_path, uid, gid)

    def getattr(self, path, fh=None):
        full_path = self._full_path(path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def readdir(self, path, fh):
        full_path = self._full_path(path)

        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        for r in dirents:
            yield r

    def readlink(self, path):
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        full_path = self._full_path(path)
        return os.rmdir(full_path)

    def mkdir(self, path, mode):
        return os.mkdir(self._full_path(path), mode)

    def statfs(self, path):
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    def unlink(self, path):
        return os.unlink(self._full_path(path))

    def symlink(self, name, target):
        return os.symlink(name, self._full_path(target))

    def rename(self, old, new):
        return os.rename(self._full_path(old), self._full_path(new))

    def link(self, target, name):
        return os.link(self._full_path(target), self._full_path(name))

    def utimens(self, path, times=None):
        return os.utime(self._full_path(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        full_path = self._full_path(path)
        print "*** open: " + full_path
        return os.open(full_path, flags)

    def create(self, path, mode, fi=None):
        full_path = self._full_path(path)
        print "*** create: " + full_path
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    # Current implementation: Whenever you read anything, it just returns whatever is in the lena_*.jpg images.
    # There's no support for multiple files yet. There will be.
    def read(self, path, length, offset, fh):
        print "*** read: " + path
        # os.lseek(fh, offset, os.SEEK_SET)

        # In attempt to not break everything,
        # read by grabbing images ONLY IF this fpath is one we've already written into images.
        # if path in self.files:
        #     file_string = self.image_filename.split(".")[0]

        #     # Compile the list of images
        #     files = []
        #     for filename in os.listdir("tmp"):
        #         if filename.startswith(file_string + "_"):
        #             files.append(filename)

        #     # Extract from each image; print output (for now)
        #     buf = []
        #     for i in range(len(files)):
        #         filename = "tmp/" + file_string + "_" + "%03i" % (i + 1) + ".jpg"

        #         #p = Popen(["java", "-jar","f6.jar", "x", filename], stdout=PIPE, stderr=PIPE)
        #         #result = p.communicate()[0]
        #         #result = check_output(["java", "-jar","f6.jar", "x", filename], stderr=self.devnull)
        #         result = os.system("java -jar f6.jar x tmp/lena_001.jpg")
        #         print result
        #         buf.append(result)

        #     return "".join(buf)
        # else:
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        print "*** write: " + path
        # os.lseek(fh, offset, os.SEEK_SET)

        if path in self.files:
            self.files[path] += buf
        else:
            self.files[path] = buf

        return os.write(self.devnull, buf)
        #return os.EX_OK

    def truncate(self, path, length, fh=None):
        full_path = self._full_path(path)
        with open(full_path, 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        return os.fsync(fh)

    def release(self, path, fh):

        if path in self.files:
            buf = self.files[path]
            # Split the buffer into chunks
            count = 0
            image_name = self.image_filename.split('.')[0]
            for chunk in grouper(4096, buf):
                chunk = "".join(chunk)  # Convert to string
                count += 1
                # Write the chunk into an image file
                str_count = "%03i" % count
                image_output_name = "tmp/" + image_name + "_" + str_count +  ".jpg"
                Popen(["java", "-jar","f6.jar", "e", "lena.jpg", image_output_name], stdin=PIPE).stdin.write(chunk)
                #p.communicate(input=chunk)[0]

        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        return self.flush(path, fh)


def main(mountpoint, root):
    FUSE(Passthrough(root), mountpoint, foreground=True)

if __name__ == '__main__':
    main(sys.argv[2], sys.argv[1])
