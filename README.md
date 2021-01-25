# matrix-to-latex

MaTrex

We are 4 Computer Science students in the Fall 2020 Software Development Class at Harvey Mudd College and we created MaTreX, a web app that converts images of matrices into LaTex Code, as our final project for the class.

Perhaps the most tedious part of using LaTeX for homework assignments is representing matrices. Our web app does the work for the user by allowing users to convert images of handwritten matrices to LaTeX code that can be copied and pasted into their own LaTeX editors. This is achieved through the use of the YOLOv5 object recognition model to classify and locate the matrix elements and a simple algorithm taking advantage of a matrix’s grid-like structure to generate the LaTeX code.

Visit our MaTreX web app and start converting your matrix images into LaTex code!
http://matrix-to-latex.herokuapp.com


The inkml2img code is taken directly from [this repo](https://github.com/RobinXL/inkml2img). The files directly taken from the repo are inkmltoimg.py and onehot.py.
