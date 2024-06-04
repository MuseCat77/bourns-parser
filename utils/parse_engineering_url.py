import re


def get_engineering_url(function_str: str):
    args_pattern = r'\"(.*?)\"|(\d+)'
    args_match = re.findall(args_pattern, function_str)
    args_match = [arg[0] if arg[0] else arg[1] for arg in args_match]
    design_url = f"https://bourns.componentsearchengine.com/entry_u_newDesign.php?\
mna={args_match[0]}&\
mpn={args_match[1]}&\
pna={args_match[2]}&\
vrq={args_match[3]}&\
fmt={args_match[4]}&\
o3={args_match[5]}&\
logo={args_match[6]}&\
lang={args_match[7]}\
&epm={args_match[8]}"
    return design_url


if __name__ == '__main__':
    print(get_engineering_url('javascript:loadPartDiv("Bourns","CR0603-PF","Bourns",1,"zip",0,"","en-US",0)'))
