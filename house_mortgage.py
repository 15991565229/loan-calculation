import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button
from matplotlib import font_manager

# reference:
# https://zhuanlan.zhihu.com/p/61140535
# https://baike.baidu.com/item/%E6%88%BF%E8%B4%B7%E8%AE%A1%E7%AE%97%E6%96%B9%E5%BC%8F/14489264
# requiremnt: python version > 3.0 python3.10 -m pip install --upgrade pip
total_loan = 100*10000
total_months = 30*12

year_lpr = 4.3*0.01
year_bp = 0.0*0.01
month_interest_rate = (year_lpr + year_bp)/12
# interest rate
# loan principal
# deng er ben jin, equal repayment
def equal_repayment_compute():
    print("total_months---",total_months)
    returned_principal = 0
    total_interset = 0
    equal_repayment = {"m_index":list(),"m_payment":list(),"m_principal":list(),"m_interest":list()}
    for month_index in range(total_months):
        month_payment = total_loan/total_months + (total_loan - returned_principal)*month_interest_rate
        month_principal = total_loan/total_months
        month_interest = (total_loan - returned_principal)*month_interest_rate
        returned_principal += month_principal
        equal_repayment["m_index"].append(month_index+1)
        equal_repayment["m_payment"].append(month_payment)
        equal_repayment["m_principal"].append(month_principal)
        equal_repayment["m_interest"].append(month_interest)
        print("======",month_index)
        # print("month index: ", month_index+1, " month_payment: ", month_payment,
        # " month_principal: ", month_principal, " month_interest: ", month_interest,
        # " returned_principal: ", returned_principal)
    total_interset = total_months*(total_months+1)*month_interest_rate*0.5
    return equal_repayment

equal_repayment = {"m_index":list(),"m_payment":list(),"m_principal":list(),"m_interest":list()}

def equal_repayment(total_loan,total_months):
    print("total_months---",total_months)
    returned_principal = 0
    total_interset = 0
    global equal_repayment
    equal_repayment = {"m_index":list(),"m_payment":list(),"m_principal":list(),"m_interest":list()}
    for month_index in range(total_months):
        month_payment = total_loan/total_months + (total_loan - returned_principal)*month_interest_rate
        month_principal = total_loan/total_months
        month_interest = (total_loan - returned_principal)*month_interest_rate
        returned_principal += month_principal
        equal_repayment["m_index"].append(month_index+1)
        equal_repayment["m_payment"].append(month_payment)
        equal_repayment["m_principal"].append(month_principal)
        equal_repayment["m_interest"].append(month_interest)
        print("======",month_index)
        # print("month index: ", month_index+1, " month_payment: ", month_payment,
        # " month_principal: ", month_principal, " month_interest: ", month_interest,
        # " returned_principal: ", returned_principal)
    total_interset = total_months*(total_months+1)*month_interest_rate*0.5
    return equal_repayment

# deng er ben xi, equal principal
def equal_principal():
    returned_principal = 0
    total_interset = 0
    equal_principal = {"m_index":list(),"m_payment":list(),"m_principal":list(),"m_interest":list()}
    for month_index in range(total_months):
        a = total_loan*np.power(month_interest_rate*(1+month_interest_rate),total_months)
        # print(a)
        b = np.power(1+month_interest_rate,total_months) - 1
        # print(b)
        month_payment = a/b
        c = total_loan*month_interest_rate*pow(1+month_interest_rate,month_index)
        month_principal = c/b
        d = total_loan*month_interest_rate*(pow(1+month_interest_rate,total_months) - pow(1+month_interest_rate,month_index))
        month_interest = d/b
        returned_principal += month_principal
        equal_principal["m_index"].append(month_index+1)
        equal_principal["m_payment"].append(month_payment)
        equal_principal["m_principal"].append(month_principal)
        equal_principal["m_interest"].append(month_interest)
        # print("month index: ", month_index+1, " month_payment: ", month_payment,
        # " month_principal: ", month_principal, " month_interest: ", month_interest,
        # " returned_principal: ", returned_principal)
    return equal_principal

def set_chinese_font():
    # plt.rcParams['font.family'] = ['sans-serif']
    # plt.rcParams['font.sans-serif'] = ['SimHei']
    # return font_manager.FontProperties(fname='simhei.ttf')
    from pylab import mpl
    print(mpl.get_cachedir())
    mpl.rcParams['font.sans-serif'] = ['Songti SC']
    mpl.rcParams['axes.unicode_minus'] = False

def config_axi(ax, x_label, y_label, title, ylim_top):  
    ax.locator_params(nbins=3)
    ax.set_xlabel(x_label, fontsize=10)
    ax.set_ylabel(y_label, fontsize=10)
    ax.set_ylim(bottom=0.,top=ylim_top)
    ax.set_title(title, fontsize=20)

def axi_plot(ax, m_index,m_principal,m_interest,principal_color,interest_color,principal_label,interest_label):

    ax.plot(m_index,m_principal,'*-',label=principal_label,color=principal_color)
    ax.plot(m_index,np.sum([m_principal,m_interest],axis=0),'*-',label=interest_label,color=interest_color)
    aera_mean = {
        principal_label: m_principal,
        interest_label: m_interest
    }
    ax.stackplot(m_index,aera_mean.values(),labels=aera_mean.keys(),colors={principal_color,interest_color})
    ax.legend(loc='upper right')

def init_plot():
    # set_chinese_font()
    fig = plt.figure('房贷分析',figsize=(16,6))
    return fig

def update_plot(equal_repayment_data,equal_principal_data):
    config_axi(ax1,'month','RMB:yuan','deng e ben jin', np.max(equal_repayment_data["m_payment"]))
    config_axi(ax2,'month','RMB:yuan','deng e ben xi',np.max(equal_repayment_data["m_payment"]))
    config_axi(ax3,'month','RMB:yuan','both',np.max(equal_repayment_data["m_payment"]))
    axi_plot(ax1,equal_repayment_data["m_index"],equal_repayment_data["m_principal"],equal_repayment_data["m_interest"],'green','red','equal_repayment_principal','equal_repayment_interset')
    axi_plot(ax2,equal_principal_data["m_index"],equal_principal_data["m_principal"],equal_principal_data["m_interest"],'green','red','equal_principal_principal','equal_pricipal_interset')
    axi_plot(ax3,equal_repayment_data["m_index"],equal_repayment_data["m_principal"],equal_repayment_data["m_interest"],'green','red','equal_repayment_principal','equal_repayment_interset')
    axi_plot(ax3,equal_principal_data["m_index"],equal_principal_data["m_principal"],equal_principal_data["m_interest"],'cyan','purple','equal_principal_principal','equal_pricipal_interset')
    plt.tight_layout()
    plt.show()

def update(val):
    print('callback update',val)
    total_loan = 100*10000
    total_months = val
    print('total_months update',val)

    total_loan = 100*10000
    equal_repayment(total_loan,total_months)
    equal_principal_data = equal_principal()
    # update_plot(equal_repayment_data,equal_principal_data)
    print('total_months update1',val)

fig = plt.figure('房贷分析',figsize=(16,6))
ax1 = plt.subplot(221)
ax2 = plt.subplot(223)
ax3 = plt.subplot(122)
# def slider_manager(fig):
init_total_loan = 100*10000
init_total_months = 30*12
# equal_repayment_data = equal_repayment()
equal_repayment = equal_repayment(total_loan,total_months)
equal_principal_data = equal_principal()
# Make a horizontal slider to control the frequency.
#fig = init_plot()
ax_month = fig.add_axes([0.25, 0.1, 0.65, 0.03])
months_slider = Slider(
    ax=ax_month,
    label='total months',
    valmin=0,
    valmax=30*12,
    valinit=init_total_months,
    valstep=[i for i in range(30*12)]
)
# register the update function with each slider
months_slider.on_changed(update)

config_axi(ax1,'month','RMB:yuan','deng e ben jin', np.max(equal_repayment["m_payment"]))
config_axi(ax2,'month','RMB:yuan','deng e ben xi',np.max(equal_repayment["m_payment"]))
config_axi(ax3,'month','RMB:yuan','both',np.max(equal_repayment["m_payment"]))
axi_plot(ax1,equal_repayment["m_index"],equal_repayment["m_principal"],equal_repayment["m_interest"],'green','red','equal_repayment_principal','equal_repayment_interset')
axi_plot(ax2,equal_principal_data["m_index"],equal_principal_data["m_principal"],equal_principal_data["m_interest"],'green','red','equal_principal_principal','equal_pricipal_interset')
axi_plot(ax3,equal_repayment["m_index"],equal_repayment["m_principal"],equal_repayment["m_interest"],'green','red','equal_repayment_principal','equal_repayment_interset')
axi_plot(ax3,equal_principal_data["m_index"],equal_principal_data["m_principal"],equal_principal_data["m_interest"],'cyan','purple','equal_principal_principal','equal_pricipal_interset')
plt.tight_layout()
plt.show()
# plt.tight_layout()
plt.show()

# def main():
    # fig = init_plot()
    # slider_manager(fig)
    # equal_repayment_data = equal_repayment()
    # equal_principal_data = equal_principal()
    # update_plot(equal_repayment_data,equal_principal_data)
    # plt.tight_layout()
    # plt.show()

# if __name__ == "__main__":
#     main()


