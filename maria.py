import os
import re
import shutil
import sys

# base_path = "./"
base_path = "./file"        #테스트용 파일이 저장된 폴더
base_target_path = "./be_sorted"    #테스트용 파일이 분류될 폴더
final_target_path = "./pre_sorted"   #테스트용 사전 정리 폴더
pre_sort_folder_list = []               #미리 정리된 폴더 목록

def get_file_list(path=base_path):
    """
    path 경로의 파일 리스트를 반납한다.
    :param path:파일 경로
    :return:파일 리스트
    """
    return os.listdir(path)

def get_penName(file_name:str):
    """
    파일명으로 부터 작가명을 추출해 낸다.
    :param file_name: 작가명이 포함된 파일 명
    :return: 작가명 str 객체
    """
    p = re.compile("\[(.*?)\]")
    result = p.findall(file_name)       #작가명이 될수 있는 후보 리스트(대게는 맨 첫번째가 작가명이다)
    #result = p.search(file_name)
    print("result : ", result)

    #작가명 처리에 대한 처리 만약 패턴을 찾아 낼수 없다면 None을 작가명으로 처리.
    if len(result) == 0:
        result = "[None]"
        return result
    else:
        result = "["+result[0]+"]"              #그렇지 않을 경우는 가장 첫번째 검색어를 작가명으로 선택

    #예외적으로 따로 명칭을 줄 작가명 리스트
    non_penNameList =  {
        "Pixiv":"CG",
        "Artist":"CG",
        "雑誌":"잡지",
        "Collection":"CG",
        "ゲームCG":"Game_CG",
        "Korean":"None",
        "Fanbox":"CG",
        "Twitter":"CG"
        }

    npnl_keys = list(non_penNameList.keys())
    # npnl_values = list(non_penNameList.values())
    # print("npnl_keys:",type(npnl_keys),npnl_keys)
    # print("npnl_values:",type(npnl_values),npnl_values)

    npldict_lower = {}
    npnl_size = len(non_penNameList)

    for i in range(npnl_size):
        npldict_lower[npnl_keys[i].lower()] = npnl_keys[i]
    # print("npldict_lower:", npldict_lower)

    # npnl_keys[0] in penNameList[0]
    for key in npnl_keys:
        low_key = key.lower()
        # print("low_key:",low_key)
        if low_key in result.lower():
            # print(key, "/", result, "/", npldict_lower[key.lower()])
            result = "["+non_penNameList[npldict_lower[low_key]]+"]"

    #선 정리 폴더 목록에 이름이 있을 경우
    for i in pre_sort_folder_list:
        if result in i:
            print("선 정리 폴더 해당")
            result = i              #선 정리된 폴더 명을 그대로 사용한다.(즉, 대가로를 사용하지 않는다)

    print("작가명:",result)
    return result

def penNameList2PathList(pen_name_list:list):
    """
    작가면 리스트를 경로 패스로 변경
    :param pen_name_list: 작가명 목록
    """
    path_list = []
    # print(pen_name_list[0:5])      #부분적으로만 출력하기
    for i in range(len(pen_name_list)):
        path_list.append(base_target_path+"/"+pen_name_list[i])
    return path_list

def mkdir(path):
    """
    path에 새로운 폴더를 생성한다.
    :param path: 생성하고자 하는 폴더
    """
    if os.path.exists(path):
        print("폴더가 존재합니다.")
        pass

    if not os.path.exists(path):
        os.makedirs(path)
        print(path, "생성완료")
        pass

def mv(source,target):
    """
    source를 target폴더에 이동한다.
    :param source: 원본 폴더 위치
    :param target: 이동하고자 하는 위치 폴더 경로
    """
    if not os.path.exists(target):
        print(source, "지정 작가명의 폴더가 존재하지 않습니다")
        pass
    elif os.path.exists(target):
        print(target+"/"+os.path.basename(source))
        if not os.path.exists(target+"/"+os.path.basename(source)):
            shutil.move(source,target)
            print(source, "이동 완료")
        elif os.path.exists(target+"/"+os.path.basename(source)):
            print("같은 이름의 파일이 이미 존재합니다.")
            pass


def make_dic(file_list:list):
    """
    파일목록으로 부터 파일명을 키로하는 작가명 사전 생성
    :param file_list: 파일목록 리스트
    :param first_one: 목록에서 가장 처음 것을 이름으로 선택한다
    :return: 파일명:작자명 사전 생성
    """
    file_dic = dict()

    for i in range(len(file_list)):
        if len(get_penName(file_list[i])) != 0:
            file_dic[file_list[i]] = get_penName(file_list[i])
        elif len(get_penName(file_list[i])) == 0:
            file_dic[file_list[i]] = "None"

    return file_dic

if __name__ == "__main__":

    #1.폴더내 파일 목록 읽어 오기
    print(len(sys.argv))
    print(sys.argv)
    #입력이 하나도 이루어지지 않았을 경우(그냥 종료)
    if len(sys.argv) <= 2:
        print("사용법 : python -m maria [정리할 폴더] [이동할 폴더] or python -m maria [정리할 폴더] [이동할 폴더] [PEN NAME을 가져올 폴더]")
        sys.exit()

    #args 입력이 두개만 이루어졌을 경우, 즉 [정리할 폴더] 와 [이동할 폴더] 만이 입력 되었을 경우
    elif len(sys.argv) == 3:
        base_path = sys.argv[1]
        base_target_path = sys.argv[2]
        print(base_path," 에서 ",base_target_path," 로 파일 정리")
        file_list = get_file_list(base_path)

    #args 입력이 세개가 이루어졌을 경우
    elif len(sys.argv) == 4:
        base_path = sys.argv[1]
        base_target_path = sys.argv[2]
        final_target_path = sys.argv[3]
        print(base_path," 에서 ",base_target_path," 로 파일 정리", "penName 목록은 ", final_target_path, "에서 가져 옴")
        file_list = get_file_list(base_path)
        pre_sort_folder_list = get_file_list(final_target_path)
    # print(file_list)
    # print("사전 정리 폴더: ", pre_sort_folder_list)

    #2.파일 목록 내 작가명 추출한 딕셔너리 만들기
    pen_dict = make_dic(file_list)
    # print(pen_dict)

    #3.작가명 리스트 생성
    pen_name_list = list(pen_dict.values())     #사전 객체에서 값(작가명) 생성
    #print(pen_name_list)
    pen_name_list = sorted(pen_name_list)       #차례대로 정렬
    #print(len(pen_name_list), pen_name_list)
    pen_name_list = list(set(pen_name_list))          #중복 사항 삭제
    #print(len(pen_name_list), pen_name_list)
    
    #4.작가명 폴더 생성
    path_list = penNameList2PathList(pen_name_list)
    # print("path_list : ", path_list)
    for i in path_list:
    #for i in path_list[0:5]:            #테스트 코드로 상위 5개만 생성
        mkdir(i)
        print("폴더 생성 : ",i)
        #pass

    #5.작가명 폴더 이동
    for i in list(pen_dict.keys()):
        source = str(base_path+"/"+i)
        target =  str(base_target_path+"/"+pen_dict[i])
        print(source,"를", target, "으로 이동")
        mv(source,target)
        pass

    #6.종료 코드
    print("코드 종료")