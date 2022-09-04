import os
import re
import shutil
import sys

# base_path = "./"
base_path = "./name_only_folder"
base_target_path = "./sorted_folder"

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
    :return: 작가명 list 객체
    """
    p = re.compile("\[(.*?)\]")
    result = p.findall(file_name)
    #print(type(result), result)
    return result

def penNameList2PathList(pen_name_list:list):
    """
    작가면 리스트를 경로 패스로 변경
    :param pen_name_list: 작가명 목록
    """
    path_list = []
    print(pen_name_list[0:5])
    for i in range(len(pen_name_list)):
        path_list.append(base_target_path+"/["+pen_name_list[i]+"]")
    return path_list

def mkdir(path):
    """
    path에 새로운 폴더를 생성한다.
    :param path: 생성하고자 하는 폴더
    """
    if not os.path.exists(path):
        os.makedirs(path)
        print(path, "생성완료")
        pass
    if os.path.exists(path):
        print("폴더가 존재합니다.")
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


def make_dic(file_list:list,first_one=True):
    """
    파일목록으로 부터 파일명을 키로하는 작가명 사전 생성
    :param file_list: 파일목록 리스트
    :param first_one: 목록에서 가장 처음 것을 이름으로 선택한다
    :return: 파일명:작자명 사전 생성
    """
    file_dic = dict()

    if first_one == True:
        for i in range(len(file_list)):
            if len(get_penName(file_list[i])) != 0:
                file_dic[file_list[i]] = get_penName(file_list[i])[0]
            elif len(get_penName(file_list[i])) == 0:
                file_dic[file_list[i]] = "None"

    #이하는 False모드에 대한 코드 구현이었으나 어차피 이름 구현시에는 맨 처음에 있는 이름을 사용함이 맞음으로 주석 처리
    # elif first_one == False:
    #     for i in range(len(file_list)):
    #         if len(get_penName(file_list[i])) != 0:
    #             file_dic[file_list[i]] = get_penName(file_list[i])
    #         elif len(get_penName(file_list[i])) == 0:
    #             file_dic[file_list[i]] = "None"

    return file_dic

if __name__ == "__main__":
    #1.폴더내 파일 목록 읽어 오기

    #print(len(sys.argv))
    if len(sys.argv) != 1:
        base_path = sys.argv[1]
        base_target_path = sys.argv[2]
    print(base_path," 에서 ",base_target_path," 로 파일 정리")
    file_list = get_file_list(base_path)
    #print(file_list)

    #2.파일 목록 내 작가명 추출한 딕셔너리 만들기
    pen_dict = make_dic(file_list)
    #print(pen_dict)

    #3.작가명 리스트 생성
    pen_name_list = list(pen_dict.values())     #사전 객체에서 값(작가명) 생성
    #print(pen_name_list)
    pen_name_list = sorted(pen_name_list)       #차례대로 정렬
    #print(len(pen_name_list), pen_name_list)
    pen_name_list = list(set(pen_name_list))          #중복 사항 삭제
    #print(len(pen_name_list), pen_name_list)
    
    #4.작가명 폴더 생성
    path_list = penNameList2PathList(pen_name_list)
    print("path_list : ",path_list)
    for i in path_list:
    #for i in path_list[0:5]:            #테스트 코드로 상위 5개만 생성
        mkdir(i)
        print(i)
        #pass

    #5.작가명 폴더 이동
    for i in list(pen_dict.keys()):
        source = str(base_path+"/"+i)
        target =  str(base_target_path+"/["+pen_dict[i]+"]")
        print(source,"를", target)
        mv(source,target)
        pass

    #6.종료 코드
    print("코드 종료")