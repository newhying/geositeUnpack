# 这是一个示例 Python 脚本。

# 按 Ctrl+F5 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import sys
import data_pb2
import ipaddress
import io

def writefile(_filepath, _str, encode):
    t_out_file = open(_filepath, "w", encoding=encode)
    t_out_file.write(_str)
    t_out_file.close()

def unpack_site(_filepath):
    uppack_str = io.StringIO()
    with open(_filepath, 'rb') as f:
        parse_sitelist = data_pb2.GeoSiteList()
        parse_data_len = parse_sitelist.ParseFromString(f.read())
        #writefile(_filepath + ".log", f'{parse_sitelist}', 'UTF-8')
        for entry in parse_sitelist.entry:
            uppack_str.write(f'{entry.country_code.lower()} :\n')
            for domain in entry.domain:
                if domain.type == data_pb2.Domain.Full:
                    uppack_str.write(f'    full:{domain.value}')
                elif domain.type == data_pb2.Domain.Regex:
                    uppack_str.write(f'    regexp:{domain.value}')
                elif domain.type == data_pb2.Domain.Plain:
                    uppack_str.write(f'    plain:{domain.value}')
                else:
                    uppack_str.write(f'    {domain.value}')
                for attribute in domain.attribute:
                    uppack_str.write(f' @{attribute.key}')
                uppack_str.write('\n')
    writefile(_filepath + ".txt", uppack_str.getvalue(), 'UTF-8')

def unpack_ip(_filepath):
    uppack_str = io.StringIO()
    with open(_filepath, 'rb') as f:
        parse_iplist = data_pb2.GeoIPList()
        parse_data_len = parse_iplist.ParseFromString(f.read())
        for entry in parse_iplist.entry:
            uppack_str.write(f'{entry.country_code.lower()} :\n')
            for cidr in entry.cidr:
                ip_len = len(cidr.ip)
                if (ip_len == 4):
                    uppack_str.write(f'    {str(ipaddress.IPv4Address(cidr.ip))}')
                elif (ip_len == 16):
                    uppack_str.write(f'    {str(ipaddress.IPv6Address(cidr.ip))}')
                if (cidr.prefix != 0):
                    uppack_str.write(f'/{cidr.prefix}')
                uppack_str.write('\n')
    writefile(_filepath + ".txt", uppack_str.getvalue(), 'UTF-8')

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    work = 0
    for argv in sys.argv[1:]:
        if (argv == '-site'):
            work = 1
        elif (argv == '-ip'):
            work = 2
        elif (work == 1):
            unpack_site(argv)
            work = 0
        elif (work == 2):
            unpack_ip(argv)
            work = 0

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
