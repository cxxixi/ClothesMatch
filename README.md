

CSE6242 Project: Taobao Clothes Matching Recommendation System
==================================================================================================



### AUTHORS:

Wendi Ren, Xi Cheng, Ren Ren and Huiying Zhu work together to complete the whole project. 

### DESCRIPTION:

This package contains two folders, Code and Doc. All the necessary code is included in the Code folder. You can find our team report and poster in the Doc folder.


	Code folder structure:
	Code/
		build_db.py
		db.py
		Clothes.sqlite
	
		scr/
			model/
				model1/
					code/
						subModel1.cpp
					output/
						output.txt
				model2/
					main.py
					util2.py
					output/
						model2_degree.txt
				img_model/
					code/
						bagword_main.py
						bagword_helper.py
						color_main.py
					imgdata/
						test/
							*.jpg
					output/
						bag_degree.txt
						color_degree.txt
			evalution/
				output/
					*_degree.txt
				evalution.py
	
		data/
			.txt
	
		html/
			static/
				css/
					*.css
				js/
					*.js
			images/
				home_img/
				res_img/

### INSTALLATION:

We suggest you install Miniconda with Python 3.6 and excute the code within a conda environment. Create a conda environment using the appropriate command. On Windows, open the installed "Conda prompt" to run this command. On MacOS or Linux, you can just use a terminal window to run the command.

```
conda create --name YOUR_ENVIRONMENT_NAME
```

This should create an environment with the name your choose. Activate it using the follow Windows command:

```
activate YOUR_ENVIRONMENT_NAME		
```

or the following MacOS/Linux command:

```
source activate YOUR_ENVIRONMENT_NAME
```

After activating the environment, make sure you install all the libaries necessary for this project including CV2.

More details on installing CV2: https://pypi.org/project/opencv-python/

### EXCUCTION:

#### Part 1: Database

You can download all the text data set at  https://tianchi.aliyun.com/getStart/information.htm?spm=5176.100067.5678.2.449675ccIJuBUR&raceId=231575, and go to src/ folder and then enter

```
python3 build_db.py
```

you will find a generated database called Clothes.sqlite, which we already built. Since the size is big, we put it at Google drive, and you can download it at https://drive.google.com/file/d/1RIVD5pxor0nbHSWdE5Kvoe2IyGO0Q3RM/view?usp=sharing and put it at the same folder with db.py (we use this function file to assist our models). 

#### Part2: Models

##### (1) Text Model 1

Go to model1/code folder, enter the following command in the terminal:

```
g++ subModel1.cpp -o subModel1
```

```
./subModel1 ../../../../data/dim_items.txt ../../../../data/dim_fashion_matchsets.txt ../../../../data/test_items.txt ../../../../data/refFile.txt ../output/recommendation.txt
```

You will find the generated recommendation.txt

For run a demo, you can replace test_items.txt with test_items_100.txt. However, it still needs to take about half of the hour. You can terminate the command so see parts of the output. The final genearted file is output.txt as we already put in the folder.

##### (2) Text Model 2

Go to model2/ folder and enter the following command in the terminal:

```
python3 main.py
```

Here, we need to use the output file of model 1. The running time is extremely long since the purchase history has very big data set. However, you can terminate the command so see parts of the output. The final genearted file is model2_degree.txt as we already put in the output/ folder.

##### (3) Image Model 1

Go to img_model/code folder.Here, we put some images to test at imgdata/test/ folder. 

To build a vocabulary, you need to download the whole image data set from https://tianchi.aliyun.com/getStart/information.htm?spm=5176.100067.5678.2.449675ccIJuBUR&raceId=231575, and make a new folder imgdata/test/ to put there image data set. However, since the image dataset are very big, so we randomly select 10000 images from these four data set and build a vocabulary called vocab.pkl, which we already put at the folder.

 With the built vocab.pkl, you can run the model by entering the following command in the terminal:

```
python3 bagword_main.py
```

The running time is still a little long since computation are not very small. However, you can terminate the command so see parts of the output at output/*.txt. The final genearted file is bag_degree.txt as we already put in the output/ folder.

##### (4) Image Model 2

Go to img_model/code folder. Entering the following command in the terminal:

```
python3 color_main.py
```

The running time is not very long. However, you can still terminate the command so see parts of the output at output/*.txt. The final genearted file is color_degree.txt as we already put in the output/ folder.

#### Part3: Visualization

To open the homepage, go to the html folder containing main.py.

Simply enter the following command in the terminal:

	python3 main.py
Open your browser with http://localhost:8888/, you now have access to the homepage!