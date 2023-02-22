import cv2
import numpy as np

def rectangle (frame,hsv_frame,low_value,up_value,color_name): 
    
    image = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    maske = cv2.inRange(image,low_value,up_value) #HSV renk aralığındaki piksel değerlerine dayalı olarak bir nesneyi tespit eder
   
    image = cv2.bitwise_and(image,frame,mask=maske)

    #opening
    image = cv2.erode(image,None,iterations=2) #erozyon,nesnenin sınırlarını aşındırarak nesneyi ön planda tutar #kernel = np.ones((3,3), dtype=np.uint8) #kernel i belirtmeseydim de 3x3 lük matris olarak alacaktı
    image = cv2.dilate(image,None,iterations=2) #dialosyaon,nesne alanını artırır ve özellikleri vurgulamak için kullanılır
    #image_opening = cv2.morphologyEx(image,cv2.MORPH_OPEN,kernel,iterations=2)

    kontur,_ = cv2.findContours(image,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) #görüntüden nesneleri algılamaya yardımıcı olur konturları çıkarmaya yardımcı olur
    
    #cv2.CHAIN_APPROX_SIMPLE bu çizginin sadece iki uç noktasına ihtiyacımız var. 
    #cv2.RETR_EXTERNAL tüm gereksiz noktaları kaldırır ve konturu sıkıştırır, böylece bellekten tasarruf sağlar.


    if len(kontur) > 0: 
        
    
        for contour in kontur:
          
            contour_area = cv2.contourArea(contour)
            if contour_area>500:
            
                cv2.drawContours(frame,contour,1,[0,225,0],thickness=3) # yeşil renkte çevresine kontur çiziyor

            
                rect = cv2.minAreaRect(contour) #maksimum noktadan çizilen konturden minimum bir en dıştaki rectangle çizdirir
                (x,y), (width,height), rotation = rect
            
                box = cv2.boxPoints(rect) 
                box = np.int64(box)
                
                cv2.drawContours(frame,[box],0,[255,0,5],thickness=3) #mavi renkte en dışına kontur çiziyor
                cv2.putText(frame,color_name, (int(x-10), int(y-10)), 0, 2, (0,0,255), 3) #renk yazısı için
        
camera = cv2.VideoCapture(0)#kameradan görüntü alıyoruz 0 ise web camden görüntü 1 ise diğer görüntü alma (hariciden)

while True: #sonsuz döngü açıyoruz kameradan alınan frameleri arka arkaya sıralasın diye
    
    red,frame = camera.read() #kameradan alınan görüntüyü(frame) okuyoruz 
    #red değeri true/false döndürür eğer okuyamadığımız bir frame olursa hata olduğunu söylememize yardımcı olur   
    #bgr kullansaydım mavi,kırmızı ve yeşili net şekilde elde ederdim  #hsv de ara renkleri daha kolay elde edeceğim için hsv ye çevirdim
    
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # alınan görüntüleri BGR dan HSV ye çevirdik
    
    height, width, _ = frame.shape #yükseklik ve genişlik 
    
    # merkezi noktaların rengini algılanması için 
    cx = int(width/2)
    cy = int(height/2)
    
    cv2.circle(frame,(cx,cy),5,(0,0,255),-1)
    
    center = hsv_frame[cy, cx] 
    hue_value = center[0] # frame in tam orta noktasındaki renkleri algılama
    print("hue value: ",hue_value)
    #cv2.putText(frame, str(hue_value), (200, 100), 0, 2, (0,0,255), 9) #renk yazısı için
   
    
    lower = np.array([100,80,80])   
    upper = np.array([140,255,255])

   
    red_low_value = np.array([0,100,100])   
    red_up_value = np.array([5,255,255])
   
    rectangle(frame,hsv_frame,red_low_value,red_up_value,color_name = "KIRMIZI")
    

    orange_low_value = np.array([6,100,100])  
    orange_up_value = np.array([22,255,255])
    
    rectangle(frame,hsv_frame,orange_low_value,orange_up_value,"TURUNCU")


    yellow_low_value = np.array([22,100,100])   
    yellow_up_value = np.array([33,255,255])
        
    rectangle(frame,hsv_frame,yellow_low_value,yellow_up_value,"SARI")


    green_low_value = np.array([38,100,100])   
    green_up_value = np.array([75,255,255])
        
    rectangle(frame,hsv_frame,green_low_value,green_up_value,"YESİL")


    blue_low_value = np.array([75,100,100])   
    blue_up_value = np.array([130,255,255])
    
    rectangle(frame,hsv_frame,blue_low_value,blue_up_value,"MAVİ")

    purple_low_value = np.array([130,100,0])   
    purple_up_value = np.array([160,255,255])
        
    
    rectangle(frame,hsv_frame,purple_low_value,purple_up_value,"MOR")
    
    #kırmızı 2 hue aralığında olduğu için ikinci defa tanımladım
    red2_low_value = np.array([160,100,100])   
    red2_up_value = np.array([179,255,255])        
    
    rectangle(frame,hsv_frame,red2_low_value,red2_up_value,"KIRMIZI")
    
    

    cv2.imshow("Frame", frame)  # burada kamera açılır tek tek sıralanan frameleri webcamden alınan görüntüleri göreceğiz
    
    key = cv2.waitKey(25)       #1 saniyede 40 frame göster
    if key & 0xFF==ord("q"):    # q tuşuna basınca çıkış yap
        break

camera.release()         # kameradan görüntü alma artık
cv2.destroyAllWindows(1)  #oluşan tüm pencereleri kapat