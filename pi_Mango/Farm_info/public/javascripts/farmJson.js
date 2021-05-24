function readJSON(file, callback) {
    let ajax = new XMLHttpRequest();
    ajax.overrideMimeType("application/json");
    ajax.open("GET", file, true);
    ajax.onreadystatechange = function () {
      if (ajax.readyState === 4 && ajax.status == "200") {
        callback(ajax.responseText);
      }
    };
    ajax.send(null);
    }

readJSON("farmData.json", function (res) {
    let data = JSON.parse(res);
    console.log(data);

    // addTable
    // 獲取table標籤元素
    let table = document.getElementById("work_table");
    
    for(i=0 ;i<=data.length-2;i++){
    // 建立新行 
    let newRow = table.insertRow();
    // 建立新單元格
    let cellZone = newRow.insertCell();
    let cellPic = newRow.insertCell();
    let cellType = newRow.insertCell();
    let cellTime = newRow.insertCell();
    let cellStatus = newRow.insertCell();
    // 向表格中插入id
    cellZone.setAttribute('id','zone'+(i+1));
    cellPic.setAttribute('id','pic'+(i+1));
    cellType.setAttribute('id','type'+(i+1));
    cellTime.setAttribute('id','time'+(i+1));
    cellStatus.setAttribute('id','status'+(i+1));
    
    // 插入font
    cellZone.setAttribute('style',"font-weight:bold");
    cellPic.setAttribute('style',"font-weight:bold");
    cellType.setAttribute('style',"font-weight:bold");
    cellTime.setAttribute('style',"font-weight:bold");
    cellStatus.setAttribute('style',"font-weight:bold");
    }

    //set zone
    for(i=0;i<=data.length-2;i++){
        console.log(data[i].zone)

        switch (data[i].zone){
        case 'A':
        document.querySelector("#zone"+(i+1)).innerHTML='<img src="images/select_A.png" alt="" border=3 height=50 width=50>'+'<font size="3" color=	#336666>區域A';	
        break;

        case 'B':
        document.querySelector("#zone"+(i+1)).innerHTML='<img src="images/select_B.png" alt="" border=3 height=50 width=50>'+'<font size="3" color=	#336666>區域B';	
        break;
    
        case 'C':
        document.querySelector("#zone"+(i+1)).innerHTML='<img src="images/select_C.png" alt="" border=3 height=50 width=50>'+'<font size="3" color=	#336666>區域C';	
        break;

        case 'D':
        document.querySelector("#zone"+(i+1)).innerHTML='<img src="images/select_D.png" alt="" border=3 height=50 width=50>'+'<font size="3" color=	#336666>區域D';	
        break;

        default:
        document.querySelector("#zone"+(i+1)).innerHTML='<font size="3" color=	#336666>無法辨識此區域';	
    }}

    // setPic
    for(i=0;i<=data.length-2;i++){
        document.querySelector("#pic"+(i+1)).innerHTML = '<img src="images/'+data[i].picNumber+'.jpg" alt="" border=3 height=100 width=100>';
    }

    
    // setType
    for(i=0;i<=data.length-2;i++){
        console.log(data[i].type)
        if(data[i].type == 0){
            document.querySelector("#type"+(i+1)).innerHTML='<img src="images/green.png" alt="" border=3 height=50 width=50>';
         }else{
            document.querySelector("#type"+(i+1)).innerHTML='<img src="images/red.gif" alt="" border=3 height=50 width=50>';
         }		
    }

    // setTime
    for(i=0;i<=data.length-2;i++){
        document.querySelector("#time"+(i+1)).innerHTML ='<font size="3" color=#336666>'+data[i].time;
    }
    // setStatus
    let str = "";
    for(i=0;i<=data.length-2;i++){
        if(data[i].type == 0){
            str ="區域正常狀態，不需擔心";
         }else{
            str ="區域需要處理" ;
         }	

        switch (data[i].zone){
        case 'A':
        document.querySelector("#status"+(i+1)).innerHTML='<font size="3" color=#336666>A'+str;	
        break;

        case 'B':
        document.querySelector("#status"+(i+1)).innerHTML='<font size="3" color=#336666>B'+str;	
        break;
    
        case 'C':
        document.querySelector("#status"+(i+1)).innerHTML='<font size="3" color=#336666>C'+str;	
        break;

        case 'D':
        document.querySelector("#status"+(i+1)).innerHTML='<font size="3" color=#336666>D'+str;	
        break;

        default:
        document.querySelector("#status"+(i+1)).innerHTML='<font size="3" color=#336666>無法辨識的'+str;	
    }}
    });