# PaymentSystem2017
Compared with the last version, the changes are listed below:
#1, the weigher module is firstly introduced to replece MyThread2_1 class (This will have effects in the place where self.thread2 and self.thread3 exist);
#2, 'try..except' statements are added to the SQL thread (the MyThread3_2_1 class);
#3， the verification of item weight is added after the SQL thread in work5 function. If the verification fails, one dialog shows until the verification successes;
#4, my customized QDialog class is introduced in the ShoppingList.py to give a message to customer;
#5, commenting the useless usage QThread.setPriority();
#6, adding the self-checking is firstly introduced into Brindley;
