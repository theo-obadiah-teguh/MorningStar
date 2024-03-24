# MorningStar

A portable Extensible Markup Language (XML) scraper designed specifically to handle Morningstar `DataWarehouse` packages. Utilizes Simple API for XML (SAX Parsing).

## Acknowledgments

The data set was provided by the Faculty of Business and Economics at the University of Hong Kong. It was part of a research programme supervised by [Prof. Yang Liu](https://www.hkubs.hku.hk/people/yang-liu/) and orchestrated by [Ms. Yaoyuan Zhang](https://www.hkubs.hku.hk/people/yaoyuan-zhang/). Additionally, I received invaluable assistance from [Mr. Zhenxian Zheng](https://github.com/zhengzhenxian) who kindly helped me through the stages of this project.  

## The Project

The task was to create a lightweight XML scraper that can be run locally on your everyday PC or laptop that could handle medium to large scale datasets with exceptional running time and performance. Afterwards, we would like to construct a MySQL database to warehouse specific subsets of the data required for the project. This will allow streamlined access for the researches to query and analyze the data. The Morningstar `DataWarehouse` was downloaded locally via a secure FTP connection.

The size of the dataset is 7.25GB in compressed `.xml.zip` format, or approximately 35.55GB in `.xml` format. The program was run on a 2020 M1 Macbook Air with 512GB SSD and 8GB RAM. The final achieved average scraping speed was 13MB/s, operating within local machine specifications, without the support of virtual machines.
