# 这是一个示例 Python 脚本。

# 按 Ctrl+F5 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import sys
import data_pb2

def writefile(_filepath, _str, encode):
    t_out_file = open(_filepath, "w", encoding=encode)
    t_out_file.write(_str)
    t_out_file.close()

def unpack_site(_filepath):
    uppack_str = ""
    with open(_filepath, 'rb') as f:
        parse_sitelist = data_pb2.GeoSiteList()
        parse_data_len = parse_sitelist.ParseFromString(f.read())
        #writefile(_filepath + ".log", f'{parse_sitelist}', 'UTF-8')
        for entry in parse_sitelist.entry:
            uppack_str += f'{entry.country_code.lower()} :\n'
            for domain in entry.domain:
                if domain.type == data_pb2.Domain.Full:
                    uppack_str += f'    full:{domain.value}'
                elif domain.type == data_pb2.Domain.Regex:
                    uppack_str += f'    regexp:{domain.value}'
                elif domain.type == data_pb2.Domain.Plain:
                    uppack_str += f'    plain:{domain.value}'
                else:
                    uppack_str += f'    {domain.value}'
                for attribute in domain.attribute:
                    uppack_str += f' @{attribute.key}'
                uppack_str += '\n'
    writefile(_filepath + ".txt", uppack_str, 'UTF-8')

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    filepath = 'z:/geosite.dat'
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    unpack_site(filepath)

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
