import os

class html_inject():
    def __init__(self, f_name):
        self.context_list = []
        self.html_file_name = f_name
        if os.path.exists(f_name):
            print('File existed rewited.')
            with open(f_name, 'r+') as html_file:
                self.file_handle = html_file
                self.html_file_lines = len(html_file.readlines())
                if self.html_file_lines != 0:
                    for line in html_file.readlines():
                        self.context_list.append(line)
                else:
                    print('File is empyt.')
        else:
            print('File not exist.')
            tmp_file = open(f_name, 'w')
            tmp_file.close()
            print('%s created.' % f_name)
    
    def file_refresh(self, ct_list):
        with open(self.html_file_name, 'w') as return_file:
            begin_context = \
'''
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Chromatogram @Itiharayuuko</title>
</head>
<body>
'''
            end_context = \
'''
</body>
</html>
'''
            return_file.write(begin_context)
            return_file.writelines(ct_list)
            return_file.write(end_context)

class html_labels():
    def __init__(self):
        self.label_context_list = []
        self.p_label_tmp = '''<span%d style="background-color:rgb%s">%s</span%d><span>&nbsp&nbsp&nbsp%s</span><br>\n'''
        self.generate_labels()

    def generate_labels(self):
        cl_rgb_list = []
        str_l = []
        temp_rgb_list = [0, 0, 0]
        index_context = 0
        for i in range(0, 3):
            while temp_rgb_list[i] < 255:
                str_l.append(str(temp_rgb_list))
                temp_rgb_list[i] += 1

        for k in str_l:
            tmp = eval(k).copy()
            if len(set(tmp)) != 1:
                cl_rgb_list.append(eval(k).copy())
                tmp.reverse()
                cl_rgb_list.append(tmp)
            else:
                cl_rgb_list.append(eval(k).copy())

        temp_rgb_list = [1, 1, 1]
        str_l = []
        for _ in range(0, 254):
            for index_li in range(0, 3):
                str_l.append(str(temp_rgb_list))
                temp_rgb_list[index_li] += 1

        cl_rgb_list.extend([eval(i) for i in str_l])

        cl_rgb_list.sort(key=self.sort_take_second_value ,reverse=False)

        for rgb_x in cl_rgb_list:
            rgb_hex_text_list = ['%02x' % j for j in rgb_x]
            rgb_hex_text = '#' + ''.join(rgb_hex_text_list)
            blank_context = '&nbsp' * 50
            rgb_hex_text_merge = rgb_hex_text + '&nbsp' * 5 + str(tuple(rgb_x))
            context_merged = self.p_label_tmp % (index_context, str(tuple(rgb_x)), blank_context, index_context, rgb_hex_text_merge)
            self.label_context_list.append(context_merged)
            index_context += 1

    def get_context_list(self):
        return self.label_context_list

    # Sort key function
    def sort_take_second_value(self, list_insert):
        return sum(list_insert)

if __name__ == "__main__":
    htx_be = html_inject('Chromatogram.html')
    htx = html_labels()
    htx_be.file_refresh(htx.get_context_list())