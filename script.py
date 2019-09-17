from bs4 import BeautifulSoup
import os.path
import sys


def crawler(orig_path, other_path):
    okbutton_id = "make-everything-ok-button"

    def has_needed_attrs(element):
        return element.has_attr("href") and element.has_attr("title") \
               and element.has_attr("onclick") and element.has_attr("rel")

    def element_path_maker(source, element):
        path_lst = [element.name]
        while element.name != 'html':
            element = element.parent
            path_lst.append(element.name)
        path_string = ' > '.join(path_lst[::-1])
        return path_string

    # Checking and open files
    if os.path.isfile(orig_path) and os.path.isfile(other_path):
        with open(orig_path) as orig, open(other_path) as other:
            orig_source = BeautifulSoup(orig, "html.parser")
            other_source = BeautifulSoup(other, "html.parser")

        # Searching of the element with required ID in origin file
        orig_okbtn_elem = orig_source.find(id=okbutton_id)

        # Searching of the related element with required attributes in another file
        for item in other_source.findAll('a', attrs={"class": orig_okbtn_elem["class"][0]}):
            if has_needed_attrs(item):
                # Adding ID for related element. It is needed to rewrite another file
                item["id"] = other_path.split('.')[0] + "-ok-button"

                # Printing the element path in output.txt file
                with open("output.txt", "w") as out:
                    out.write(element_path_maker(other_source, item))
    else:
        print("The file doesn't exist!")


if __name__ == "__main__":
    crawler(sys.argv[1], sys.argv[2])
