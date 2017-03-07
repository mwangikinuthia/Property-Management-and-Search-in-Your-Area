'''we use this part to rank our properties with services provided and amenities'''
#to rank we must call  plot_rating(),house_ranking() in a shell or a custom commmand
from .models import houseDesc,Plot
def plot_rank(plot):
    S_R={'Very safe':4,'Safe':3,'Good':2 ,'Worrying':1}
    W_R={'More than 5 days PW':4,'Thrice Per week':3,'Once Per week':2,'Not Available':0}    
    wr=plot.water_availabity
    sr=plot.location_security
    aa=plot.No_of_houses
    bb=plot.availableHouses
    ocr=float(bb)/float(aa) * 4
    final=(ocr+S_R.get(sr)+W_R.get(wr))/3 + 0.3+10
    return final   
def plot_rating():
    ids=[]
    plots=Plot.objects.filter(status='approved')
    for plot in plots:
	ids.append(plot.id)
    for i in range(len(ids)):
	plot_=Plot.objects.get(id=ids[i])
	plot=Plot.approved.filter(id=ids[i])
	y=plot_rank(plot_)
	plot.update(points=y)
    return '****Done rating****'
	
def house_points(house):
    a_r={'Water and Electricity':2, 'Water only':3,'Electricity only':3,'Nothing':5}
    b=house.booking.count()*5
    hse_r=house.house_bills
    a_r_p=a_r.get(hse_r)
  
    if house.comment.count() <= 10:
            cp=3
    elif house.comment.count() >10:
                cp=5
    else:
                cp=1
    points=+cp+b+a_r_p+10
    return points

def house_ranking():
	""" property rank""""
    houses_id=[]
    houses=houseDesc.approved.all()
    for house in houses:
	houses_id.append(house.id)
    for i in range(len(houses_id)):
	    house_=houseDesc.objects.get(id=houses_id[i])
	    house=houseDesc.approved.filter(id=houses_id[i])
	    y=house_points(house_)
	    house.update(points=y) 
    return '********Done house ranking**********'
    
