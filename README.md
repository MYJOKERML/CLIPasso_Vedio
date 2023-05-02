# CLIPasso_Vedio

This is a project based on [CLIPasso](https://clipasso.github.io/clipasso/) and [RIFE](https://github.com/megvii-research/ECCV2022-RIFE). In this project, you can turn a vedio into an interesting simple stroke video.

![np2v4-cazko](https://cdn.jsdelivr.net/gh/MYJOKERML/imgbed//taishi/output_64X_64fps.gif)


# How to use it

1. Install dependent environment. Recommend anaconda.

   ```
   conda create --name clipasso_vedio python=3.7
   conda activate clipasso_vedio
   git clone https://github.com/MYJOKERML/CLIPasso_Vedio.git
   cd CLIPasso_Vedio
   pip install -r requirements.txt
   cd CLIPasso
   pip install torch==1.7.1+cu101 torchvision==0.8.2+cu101 -f https://download.pytorch.org/whl/torch_stable.html
   pip install git+https://github.com/openai/CLIP.git
   git clone https://github.com/BachiLi/diffvg
   cd diffvg
   git submodule update --init --recursive
   python setup.py install
   cd ../../
   ```

2. Put your video in the folder `input` and then run the project.

   ```
   python main.py --target_file your_file_name
   ```

   



