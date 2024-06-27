新建一个叫hg3的文件夹，把hg3都丢进去   

先用WGC_en，把hg3批量转换为png   
①setting里选PNG，所有勾去掉，   
②点击output directry，选择第一个，打勾create foler。   
③点convert all   

接着用hg3_offgen，生成对应hg3的ps图层文件夹，python hg3_offgen.py hg3   

打开ps，文件-脚本-将脚本载入堆栈，浏览选择文件夹内所有图片，点确定   

文件-脚本-浏览，选择layer_rename.jsx，将所有图层重命名。保存psd   

重新打开一个WGC_en，把psd拖入，设置，输出格式选hg3，勾上第一第四个单选框，其他不勾，直接转换即可   
