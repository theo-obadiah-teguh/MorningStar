# MorningStar
An ETL pipeline designed specifically to handle Morningstar `DataWarehouse` packages. Utilizes Python 'iterparse' ElementTree, which is similar to SAX Parsing for extraction and transformation, and AWS RDS MySQL as the load target.

## Acknowledgments

The data set was provided by the Faculty of Business and Economics at the University of Hong Kong. It was part of a research programme supervised by [Prof. Yang Liu](https://www.hkubs.hku.hk/people/yang-liu/) and orchestrated by [Ms. Yaoyuan Zhang](https://www.hkubs.hku.hk/people/yaoyuan-zhang/). Additionally, I received invaluable assistance from [Mr. Zhenxian Zheng](https://github.com/zhengzhenxian) who kindly helped me through the stages of this project.  

## The Project

The task was to create a lightweight XML scraper that can be run locally on your everyday PC or laptop that could handle medium to large scale datasets with exceptional running time and performance. Afterwards, we would like to construct a MySQL database to warehouse specific subsets of the data required for the project. This will allow streamlined access for the researches to query and analyze the data. The Morningstar `DataWarehouse` was downloaded locally via a secure FTP connection.

The size of the dataset is 7.25GB in compressed `.xml.zip` format, or approximately 35.55GB in `.xml` format. The program was run on a 2020 M1 Macbook Air with 512GB SSD and 8GB RAM. The final achieved average scraping speed was 13MB/s, operating within local machine specifications, without the support of virtual machines.

## New Updates
I decided to add AWS connectivity to the entire build. Now, the data will instead be pipelined to a fresh AWS RDS MySQL server. This was not part of the original implementation; however, it makes more sense if we had a huge team with multiple developers. 

## Room for Improvement
Although the majority of the script runs in very reasonable time, the caveat of this cloud implementation may actually be the AWS `db.t3.micro` hardware. As it only has 1 GiB of RAM, it becomes a bottleneck during the loading phase. The script `pop_db.sql` populates the database with a `LOAD DATA LOCAL INFILE` command. Performance in this section drops compared to the original local implementation. 

In the future, better hardware could facilitate speed and performance of this data pipeline. Additionally, the whole data extraction and transformation process could be run from a faster AWS EC2 instance.

## Compilation and Execution Instructions:
1. Make sure you have Git and Python installed on your device (as well as a few freely available Python libraries).
1. Open your terminal, choose your desired directory and clone the repository by executing `git clone https://github.com/theo-obadiah-teguh/MorningStar.git`.
1. Enter your GitHub username and token (if applicable).
1. Open `main.py` in the "Build" folder and make sure the `source_path` variable is consistent with the data's location on your device.
1. Run `chmod +x exec.sh` to give execution permissions to the main file.
1. Acquire and download an AWS CA certificate.
1. Create a `.env` file with the following variables:
   - `RDS_HOST` : The host link of the database provided by AWS.
   - `RDS_USER` : The username coressponding to the database.
   - `RDS_PASS` : The password coressponding to the username.
   - `RDS_CA`   : The path to the `global-bundle.pem` CA certificate.
1. Execute `./exec.sh` to run the program.
