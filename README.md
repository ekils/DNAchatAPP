# DNAchatAPP
最新版本，可以正常聊天，並且從資料庫讀取聊天記錄。如同line,slack依樣。 </br>

![GitHub Logo](https://github.com/ekils/DNAchatAPP/blob/master/DNAjango/Theme-Shield/img/0810.gif)




<h3>* Before 07/11 : </h3></br>
                 1. Understanding docker, restAPI,Redis and prepare resources. </br>
                 2. Setting up Django for pycharm (Ref: https://www.jetbrains.com/help/pycharm/using-docker-compose-as-a-remote-interpreter-1.html)</br>
                 3. Setting up chatapp project(Ref: https://channels.readthedocs.io/en/latest/tutorial/part_1.html, and  https://github.com/twtrubiks/django-channels2-tutorial)</br>
                 4. Setting up docker envirenment (docker-compose , dockerfile and requirement.txt).</br>
                 5. Setting up database from default sqlite to Mysql (from docker)</br>
                 6. Setting up bootstrap for Django (Ref : https://blog.csdn.net/qingche456/article/details/68491292 )</br>
                 7. Finish login page, signup page and main page.</br>
                 8. Finish personal-id by uuid setting.</br>
<h3>* 07/12 : </h3></br>
                1. Finish bootstrap modal window with jquery and ajax value passing.</br>
<h3>* 07/17 : </h3></br>
                1. Add friend request from backend to frontend (views.py get data from models and pass to html) </br>
                2. Ajax update data witout refresh page and jquery clean textarea, and clean update.</br>
                3. Solve while "send add friend request" can  access to mysql data and use unique key to construct the relationship.</br>
<h3>* 07/19 : </h3></br>  
                1. Modify html UI for more good UX.(Side-bar created.) </br>
<h3>* 08/03 : </h3></br>  
                1. Change background color. </br>
                2. Solve string pass through websocket to frondend async problem. </br>
                3. Change input to textarea for multi text-line and fix keypress by default. (Ref:https://blog.csdn.net/hj7jay/article/details/74279967)</br>
                4. Solve messages float right and left problems. (Ref:https://bootsnipp.com/snippets/exR5v , and https://jsfiddle.net/dty6w2eh/37/) </br>
                5. Solve output paragraph problems. </br>
                
<h3>* 08/08 : </h3></br> 
                1. Solve jquery scroll top problem. (Ref:https://stackoverflow.com/questions/24450304/load-data-on-scroll-up-like-facebook-chatting-system/24450518) </br>
                2. Fix chat messages load logs.</br>
                3. Add message logs sql databases.</br>
                4. Solve jquery infinite load bug. ($('.messages').scrollTop(2000);})

<h3>* 08/09 : </h3></br> 
                1. Fix bugs: messages logs which should shows up by sender_id with right part(side).</br> 
                2. Modified mysql database for mwssages log.</br> 
                3. Fix for loop id variables can not get problems.(Ref:https://stackoverflow.com/questions/33643239/accessing-an-element-in-django-for-loop)</br>
                
<h3>* 08/10 : </h3></br> 
                1. Minor bugs fixed.</br> 
                2. Basic chat version is worked!</br> 

<h3>* 08/10 : </h3></br> 
                1. Minor bugs fixed.</br> 

<h1>* To be continued </h1></br>
1. Deployed to nginx.</br>
2. Support sending pics and media files.</br>
3. Broadcasting for trending social media( eg. IG,FB.....)</br>




<h1>* Other Refrences </h1></br>
*creating-the-chat-app (Ref:https://channels.readthedocs.io/en/latest/tutorial/part_1.html#creating-the-chat-app )</br>
* Configuring Remote Interpreter via DockerCompose (Ref: https://www.jetbrains.com/help/pycharm/using-docker-compose-as-a-remote-interpreter.html#docker-compose-remote)</br>
* django视图-使用TemplateView快速运行一个bootstrap网页 (Ref: https://blog.csdn.net/qingche456/article/details/68491292)</br>
* How to Insert Data into a Database from an HTML form in Django (Ref:http://www.learningaboutelectronics.com/Articles/How-to-insert-data-into-a-database-from-an-HTML-form-in-Django.php)</br>
*Performing raw SQL queries (Ref: https://docs.djangoproject.com/en/1.11/topics/db/sql/#executing-custom-sql-directly) </br>
* Django- Print data in html (in app2) from model (in app1) (Ref: https://stackoverflow.com/questions/28988681/django-print-data-in-html-in-app2-from-model-in-app1)</br>
