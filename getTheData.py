import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


wd = webdriver.Edge(r"msedgedriver.exe")

def getPostId(wd):
  element = wd.find_element(By.TAG_NAME,'body')
  classList = str(element.get_attribute('class')).split(' ')
  return  classList[3][7:]

def getData():
    df = pd.read_excel("Input.xlsx")
    n,m = df.shape
    dic=[]
    for i in range(0,n):
        print(i)
        dic.append({})
        URL = df['URL'][i]

        dic[i]['URL_ID'] = df['URL_ID'][i]
        try:
            # get the title of the article
            wd.get(URL)
            postId = getPostId(wd)
            time.sleep(.1)
            x_pathTitle = f'//*[@id="post-{postId}"]/div[1]/div[1]/div[2]/div[2]/header/h1'
            # //*[@id="post-3150"]/div[1]/div[1]/div[2]/div[2]/header/h1
            dic[i]["title"] = wd.find_element(By.XPATH, x_pathTitle).text
            print(f'---------->  {dic[i]["title"]}')
            # get all the content from the article
            x_pathContent = f'//*[@id="post-{postId}"]/div[2]/div/div[1]/div/div[2]'
            textList = str(wd.find_element(By.XPATH, x_pathContent).text).split("\n")

            # get the extra content from the article
            x_extra = f'//*[@id="post-{postId}"]/div[2]/div/div[1]/div/div[2]/pre'  
            x_extra2 =f'//*[@id="post-{postId}"]/div[2]/div/div[1]/div/div[2]/div[1]'
            x_extra3 =f'//*[@id="post-{postId}"]/div[2]/div/div[1]/div/div[2]/div[2]'
            ExtraList = str(wd.find_element(By.XPATH, x_pathContent).find_element(By.XPATH, x_extra).text).split("\n")
            ExtraList.extend(str(wd.find_element(By.XPATH, x_pathContent).find_element(By.XPATH, x_extra2).text).split("\n"))
            ExtraList.extend(str(wd.find_element(By.XPATH, x_pathContent).find_element(By.XPATH, x_extra3).text).split("\n"))

            # Removing the extra content from the article content
            for element in ExtraList:
                if element in textList:
                    textList.remove(element)
                    
            # store the complete content in a single string
            dic[i]['content'] = ""
            
            for j in textList:
                dic[i]['content'] += j
                dic[i]['content'] += '\n'
            
        except:
            dic[i]["title"] = "UNABLE TO GET THE CONTENT FOR THE URL"
            dic[i]['content'] = "Some Error occured while getting the url"

    # Write the data in .txt format file
    print("Got the data ---------------------------------------------------")
    j= 0
    for i in dic:
        # try:
        #     try:
        #         URLfile = open(f'articleData\{i["URL_ID"]}.txt', 'w')
        #         URLfile.writelines(i['title'])
        #         URLfile.writelines('\n')
        #         URLfile.writelines(i['content'])
        #         URLfile.close()
        #     except:
        #         print(j)
        #         print(i['content'])
        #         print('got error here')    
        # except:
        #     print(j)
        #     print('Unable to print too')
        # j += 1
        URLfile = open(f'articleData\{i["URL_ID"]}.txt', 'w',encoding="utf-8")
        URLfile.writelines(i['title'])
        URLfile.writelines('\n')
        URLfile.writelines(i['content'])
        URLfile.close()
    
    wd.quit()
    


if __name__ == "__main__":
    getData()