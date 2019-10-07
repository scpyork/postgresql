
### Select all data from the countries table (list only 10)
    scpdata=> SELECT * FROM countries LIMIT 10;
     country_code |          country           | m49 | iso2 | iso3
    --------------+----------------------------+-----+------+------
                1 | Armenia                    | 51  | AM   | ARM
               10 | Australia                  | 36  | AU   | AUS
              100 | India                      | 356 | IN   | IND
              101 | Indonesia                  | 360 | ID   | IDN
              102 | Iran (Islamic Republic of) | 364 | IR   | IRN
              103 | Iraq                       | 368 | IQ   | IRQ
              104 | Ireland                    | 372 | IE   | IRL
              105 | Israel                     | 376 | IL   | ISR
              106 | Italy                      | 380 | IT   | ITA
              107 | Côte d'Ivoire              | 384 | CI   | CIV
    (10 rows)

## Asigning an alias in the query
We may wish to shorten the name of what we are querying to save typing later on. Here we give the commodity balance production table the name `p`
and ask for results only where the year matches the number 2013. This time we limit our results to 5.

    SELECT * FROM cb_production p WHERE p.year=2013  LIMIT 5;

    scpdata=> SELECT * FROM cb_production p WHERE p.year=2013  LIMIT 5;
     area_code | item_code | year |  unit  |     value     | flag
    -----------+-----------+------+--------+---------------+------
             2 |      2617 | 2013 | tonnes |  78597.000000 | S
             2 |      2513 | 2013 | tonnes | 514000.000000 | S
             2 |      2600 | 2013 | tonnes | 441732.000000 | S
             2 |      2614 | 2013 | tonnes |   3000.000000 | S
             2 |      2661 | 2013 | tonnes |  13917.000000 | S
    (5 rows)

As we can see we have our result, however we may also want to know what the items selected within these correspond to. To do this we can link multiple tables with the join command. 


## Link two tables
Sometimes we wish to combign two tables to produce an output. We can do this through one of the many possible join commands.



    scpdata=> SELECT * FROM cb_production p JOIN items i ON(p.item_code = i.item_code) WHERE p.year=2013  LIMIT 10;


     area_code | item_code | year |  unit  |     value     | flag | item_code |              item               
    -----------+-----------+------+--------+---------------+------+-----------+---------------------------------
             2 |      2617 | 2013 | tonnes |  78597.000000 | S    |      2617 | Apples and products
             2 |      2513 | 2013 | tonnes | 514000.000000 | S    |      2513 | Barley and products
             2 |      2600 | 2013 | tonnes | 441732.000000 | S    |      2600 | Brans
             2 |      2614 | 2013 | tonnes |   3000.000000 | S    |      2614 | Citrus, Other
             2 |      2661 | 2013 | tonnes |  13917.000000 | S    |      2661 | Cotton lint
             2 |      2559 | 2013 | tonnes |  27412.000000 | S    |      2559 | Cottonseed
             2 |      2594 | 2013 | tonnes |  11769.000000 | S    |      2594 | Cottonseed Cake
             2 |      2575 | 2013 | tonnes |   4707.000000 | S    |      2575 | Cottonseed Oil
             2 |      2625 | 2013 | tonnes | 303788.000000 | S    |      2625 | Fruits, Other
             2 |      2620 | 2013 | tonnes | 610570.000000 | S    |      2620 | Grapes and products (excl wine)
    (10 rows)
