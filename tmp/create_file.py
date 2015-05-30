import json
import os

file_table = '{}'
file_table_json = json.loads(file_table)



list_of_image_strings = ['lena.jpg']
image_counter = 0

def grouper(n, iterable):
    it = iter(iterable)
    while True:
       chunk = list(itertools.islice(it, n))
       if not chunk:
           return
       yield chunk


def create_entry(full_path):

  page_table = []
    # Split the buffer into chunks
  count = 0
  buf = os.system("cat " + full_path)
  chunks = grouper(4096, buf)
  for chunk in chunks:
    chunk = "".join(chunk)  # Convert to string
    count += 1
    # Write the chunk into an image file
    image_name = list_of_image_strings[image_counter % len(list_of_image_strings)].split(".")[0]
    image_counter += 1
    image_output_name = image_name + "_" + str(count) +  ".jpg"

    page_entry = '{}'
    page_entry = json.loads(page_entry)

    p = Popen(["java", "-jar","f6.jar", "e", self.image_filename, "upload_pics/" + image_output_name], stdin=PIPE)

    os.system("python upload_pics/uploadr.py")


    #page_entry['url'] =
    #page_entry['id'] =
    #page_entry['dirty_bit'] =

    page_table.append(page_entry)

  file_table_json[full_path] = page_table
    #print p.communicate(input=chunk)[0]


  file_table_json[full_path] = page_table


create_entry("message.txt")