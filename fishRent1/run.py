# -*- coding: utf-8 -*-
import draw
import rent_analyse
import rentspider


if __name__ == '__main__':
    print("开始总程序")
    Filename = "rent.csv"
    rentspider.run()
    all_list = rent_analyse.spark_analyse(Filename)
    draw.draw_bar(all_list)
    print("结束总程序")
