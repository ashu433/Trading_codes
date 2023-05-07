def calculator_stock_market_long(buy_price,stop_loss,quantity):
    brokerage_min=0.0003
    brokerage_max=20
    stt=0.00025
    turn_over_charges=0.000001
    transaction_charge=0.0000345
    stamp_duty=0.00003
    GST=0.18

    stt_charges=stt*quantity*stop_loss
    SEBI_turn_over_chrgaes=(buy_price+stop_loss)*quantity*turn_over_charges
    transaction_charge=(buy_price+stop_loss)*quantity*transaction_charge
    stamp_duty_charges=buy_price*quantity*stamp_duty

    buy_brokerage=buy_price*quantity*brokerage_min
    sell_brokerage=stop_loss*quantity*brokerage_min

    if (buy_brokerage<20):
        brokerage_buy_net=buy_brokerage
    else:
        brokerage_buy_net=20

    if (sell_brokerage<20):
        brokerage_sell_net=sell_brokerage
    else:
        brokerage_sell_net=20

    tax=(brokerage_buy_net+brokerage_sell_net+transaction_charge)*GST

    toatl_brokerage=brokerage_buy_net+brokerage_sell_net

    net_charges=toatl_brokerage+tax+stt_charges+SEBI_turn_over_chrgaes+transaction_charge+stamp_duty_charges

    net_buy_value=buy_price*quantity
    net_sell_value=stop_loss*quantity-net_charges

    profit=((net_sell_value-net_buy_value)/net_buy_value)*100
    overall_profit=net_sell_value-net_buy_value

    return profit,overall_profit

def calculator_stock_market_short(buy_price,stop_loss,quantity):
    brokerage_min=0.0003
    brokerage_max=20
    stt=0.00025
    turn_over_charges=0.000001
    transaction_charge=0.0000345
    stamp_duty=0.00003
    GST=0.18

    stt_charges=stt*quantity*buy_price
    SEBI_turn_over_chrgaes=(buy_price+stop_loss)*quantity*turn_over_charges
    transaction_charge=(buy_price+stop_loss)*quantity*transaction_charge
    stamp_duty_charges=stop_loss*quantity*stamp_duty

    buy_brokerage=buy_price*quantity*brokerage_min
    sell_brokerage=stop_loss*quantity*brokerage_min

    if (buy_brokerage<20):
        brokerage_buy_net=buy_brokerage
    else:
        brokerage_buy_net=20

    if (sell_brokerage<20):
        brokerage_sell_net=sell_brokerage
    else:
        brokerage_sell_net=20

    tax=(brokerage_buy_net+brokerage_sell_net+transaction_charge)*GST

    toatl_brokerage=brokerage_buy_net+brokerage_sell_net

    net_charges=toatl_brokerage+tax+stt_charges+SEBI_turn_over_chrgaes+transaction_charge+stamp_duty_charges

    net_sell_value=buy_price*quantity
    net_buy_value=stop_loss*quantity+net_charges

    profit=((net_sell_value-net_buy_value)/net_sell_value)*100
    overall_profit=net_buy_value-net_sell_value

    return profit,overall_profit




if __name__=='__main__':  
    pass