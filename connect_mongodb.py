import pymongo
from pymongo.server_api import ServerApi

uri = "mongodb+srv://victoria91718:white0718@poxa.1j2eh.mongodb.net/?retryWrites=true&w=majority&appName=poxa"
client = pymongo.MongoClient(uri)
# client = pymongo.MongoClient(uri, server_api=ServerApi('1'))

mydb = client["WebInformation"]
mycol = mydb["article"]

mydata = {
        "title": "POXA 2024 7/29 每週動態",
        "content": "感謝訂閱POXA Info 每週最新動態！E-dReg價格站回600元/MWh，投標量最低只剩170.8MW，花黑噴？8月需求曲線公布，需求量上限增加17.7MW！除了需求曲線，E-dReg還有哪些規則更新，詳細內容請看本週主題分析。",
        "labels": {
            "0": "規範解析",
            "1": "E-dReg"
        },
        "subtitle": {
            "0": "📢 台電最新公告",
            "1": "🎓 本週主題分析",
            "2": "📈 市場最新動態",
            "3": "💡 台電電力供需資料",
            "4": "POXA ENERGY 專屬分析 🧐",
            "5": "📚 資訊來源網站"
        },
        "subcontent": {
            "0": "7/23 修正「公告事項 4-3：日前輔助服務市場需求量估算方式說明文件」。",
            "1": "本週調頻備轉擴增至786.4MW，價格連續185天維持0元，平均得標率降至63.6%，影響整體收益； 即時與補充價格呈現下跌，主因颱風天用電量減少，整體供給增加，應為短期現象； E-dReg在需求曲線實施後，價格降至500元/MWh，得標量升至292.8MW，但7月26日價格突然回升至600元/MWh， 因投標量減少至170.8MW，使最高願付價格上升，都是凱米惹得禍，截稿前回升到184.8MW，市場變化引人關注； 平台公告8月需求曲線，需求量上限增加17.7MW； 7月22日E-dReg規則修改，除了需求曲線機制外，也包括報價機制及技術規格要求，包括電能移轉量上限、升降載率設定及系統頻率達59.50Hz以下的作動方式， 詳細內容都在本週的主題分析。",
            "2": "「調頻服務」平均結清價格維持在0元/MWh； 目前累計參與容量擴增786.4MW，較上週增加4.2MW，來自於1家現有廠商盛齊綠能，盛齊綠能排名上升1名，成為第3名。\n「E-dReg」平均結清價格從600元/MWh下滑到557.14元/MWh，下滑7.14%，主要是7/22需求曲線實施，價格下降到500元/MWh； 目前累計參與容量維持在293.8MW，本週沒有新增合格交易者與參與容量。\n「即時備轉」平均結清價從256.54元/MWh下滑到237.1元/MWh，大幅下滑7.58%，終止連兩週小幅上升，研判是這週颱風到來，用電量減少，整體供給上升所致； 目前累計參與容量維持138MW，本週沒有新增合格交易者與參與容量。\n「補充備轉」平均結清價格從209.1元/MWh下滑到202.03元/MWh，下滑3.38%，同樣受整體供給上升影響； 目前累計參與容量減少至319.7MW，較上週減少1.2MW，來自於1家現有廠商昱衡能源，昱衡能源目前也退出輔助服務市場。",
            "3": "本週再生能源佔比12%，最高滲透率來到29.56%，反而都較上週增加，主要是颱風因素，整體用電負載減少的關係。",
            "4": "分析電網頻率及供需變化對dReg/sReg儲能充放電排程的影響。",
            "5": "整理各種POXA定期追蹤的原始資料來源網站。"
        },
        "section": {
            "0": [
                "7/23 修正「公告事項 4-3：日前輔助服務市場需求量估算方式說明文件」。主要配合本次「電力交易平台管理規範及作業程序」之修正，移除公告事項4-3中關於E-dReg需求量估算方式的規定。"
            ],
            "1": [
                "POXA基地在新竹，看到中南部有不少災情，希望大家都能平安無事🙏。 本週調頻備轉擴增至786.4MW，價格連續185天維持0元，平均得標率降至63.6%，持續影響整體收益； 即時與補充本週都是下跌的，主要是因為颱風天，用電量減少，整體供給上升，應該是短期現象；",
                "E-dReg在7/22需求曲線實施後，價格下滑至500元/MWh，但得標量最高升到292.8MW，與預期相符！ 但令人意外的是從7/26開始價格開高回升到600元/MWh，主要是整體投標量大幅減少至170.8MW，使得最高願付價格上升。",
                "這投標量的巨幅震盪，讓價格又重回甜甜價，也驗證了投標量與最高願付價格的關係，老編發現投標量低於220MW的當下，第一個反應就是有人投600元/MWh嗎？ 這次是神機妙算？或是合作無間？抑或是又是大哥扛?市場的變化真是令人好奇啊👀 從時間軸來看，應該是凱米惹得禍，至於災情嚴不嚴重？或是真相如何？就看後續何時投標量可以回復正常了，截稿前投標量還是184.8MW，雖然有慢慢復甦， 但還差了100多MW，POXA後續會持續追蹤最新進展。",
                "另外一個本週大事，就是平台公告了8月的需求曲線，7月的需求曲線，第二段500元的尾端在353.3MW，而8月的需求曲線延長到360.8MW，500元/MWh的第二段多了7.5MW， 而第三段尾端，從544.9MW(對應84.1元/MWh)增加到562.6MW(對應75.7元/MWh)，也就是需求量上限增加了17.7MW， 都有小幅增加。 照台電說法，未來可能一次公布往後3個月的E-dReg需求曲線，可以有更多資訊評估需求量的變化趨勢。",
                "後續E-dReg需求曲線的變化，還需持續觀察：",
                "需求曲線的每月變化趨勢：需求量的增長速度？只增不減還是是否受季節因素影響？\n2025或是更長期的需求曲線變化趨勢：還是需求垂直線時，之前台電是說2025會到500MW，那改成需求曲線後，最大需求量會延伸到哪？ POXA會持續追蹤並推敲預測一下。",
                "接下來，延續上週E-dReg的改版，除了需求曲線外，E-dReg還改了哪些東西？",
                "這次修改主要有3個重點，底下分別說明：",
                "E-dReg需求曲線機制\nE-dReg報價機制\nE-dReg技術規格要求，包括：電能移轉量上限、升降載率設定、及遇系統頻率達59.50Hz以下情事之作動方式。",
                "1. E-dReg需求曲線機制",
                "而附件九如下：",
                "大概就跟之前說的差不多，只是更具體，像是最小變動單位為0.1MW，然後曲線尾端有個需求量上限。 而需求量上限還是相對模糊，『係以統計方法分析系統淨負載尖離峰差異之成長趨勢後調整，以達成本公司系統可靠度之目標。』， 但可以肯定的是，需求量上限會反應實際需求，那是不是表示就有可能低於或超過，當初台電政策宣告的2025 500MW呢？ 後續POXA會計算這兩年的淨負載尖離峰差異，來看看與需求量上限變化的關聯👀。",
                "2. E-dReg報價機制",
                "報價代碼於單一調度日內各報價區間提出之報價應為一致，也就是同一天你報600元/MWh，那整天都是600元/MWh，不可以上午600元/MWh，下午500元/MWh； 這裡要注意的是，補充說明有強調報價包含價格跟容量，所以不只是價格，連容量也要一致，也就是你不能上午投10MW，下午投5MW或0MW。 而價錢跟容量都要一致，目的應該是要確保整日的得標量是一致的，這樣台電才比較容易去做全日電能移轉排程。",
                "3. E-dReg技術規格要求",
                "E-dReg的充放電規則做了一些修改，主要是為了符合電力調度及系統穩定需求，修正附件六有關E-dReg之技術規格要求，依序為大家說明：",
                "刪除排程指定或調度指令(電能移轉)容量不超過得標容量50%之限制規定。\n要求(電能移轉)升降載率設定，以避免大量E-dReg作動反不利全系統運轉穩定。\n修正同時執行(電能移轉充電及動態調節模式)遇系統頻率達59.50Hz以下情事之作動方式。",
                "排程的容量上限從得標容量的50%增加至得標容量，也就是說以往是最多充50%得標容量，可以連續充4個小時， 現在變成也可以連續充電100%得標容量2個小時，具有更大的調度彈性。另外，緊急調度的排程同樣沒有50%的限制。",
                "再來是升降載率設定，當你轉換不同電能移轉排程容量時，要慢慢升降輸出功率，這個規則是為了避免大量E-dReg作動，導致系統頻率過快變化，影響系統穩定， 詳細規定可以參考「公告事項 3-6：E-dReg執行電能移轉升降載率設定說明文件」，後面會有POXA的整理說明。",
                "最後是低頻事件的處理，低頻事件的定義是『執行電能移轉之充電模式時，若系統頻率達59.50Hz以下』就會觸發，觸發後，取消當下及下一個15分鐘的電能移轉排程， 進入動態調頻模式，關於低頻事件的詳細規則，可以參考「公告事項3-7：E-dReg遇59.50Hz作動模式說明文件」。",
                "這次算是補完了E-dReg的控制規則，不同模式的切換要不要執行升降載率？事件的優先權？都在這次的規則裡面有了明確的定義。 E-dReg共有四種模式：",
                "模式一(動態調頻模式)：就是執行dReg0.5。\n模式二(電能移轉模式)：就是同時執行電能移轉及動態調節dReg0.5。\n模式三(緊急調度事件)：接到緊急調度指令，執行特定的充放電排程。\n模式四(低頻事件)：執行電能移轉或緊急調度之充電模式時，若系統頻率達59.50Hz以下，就會觸發，進入動態調頻模式。",
                "我們先講升降載率，再講模式優先權。 在多數時間，E-dReg只會在模式一跟二切換，當模式一進入模式二，或是模式二進入模式一，這時候就要慢慢升降載， 另外在模式二，切換不同排程量時，也要慢慢升降載率，避免系統頻率變化太快，影響系統穩定，這裡升降載都是5分鐘內達到目標值， 像下圖的例子，每次15分鐘切換排程時，都要慢慢升降載率，例如：0MW → 2MW → 5MW → 3MW → 5MW → 0MW，如規範下圖所示：",
                "而模式三的緊急調度的觸發跟結束，不受升降載率的限制，會馬上升到目標值，結束後會馬上降到0MW，不過緊急調度當下15分鐘的剩餘排程會取消， 也就是剩餘排程會變成0MW的排程，也就是模式一的動態調頻，若是下一個時段是模式二，就要服從升降載率的規則，如規範下圖所示：",
                "最後剩下模式四的低頻事件，當觸發低頻事件時，會立即中止該時段電能移轉跟緊急調度的排程，以及下一個時段的排程，進入模式一，也就是動態調頻模式(0MW的排程量)， 注意，這邊比模式三多休息一個時段喔， 而休息結束後，若是下一個時段是模式二，同樣要服從升降載率的規則，如規範下圖所示：",
                "介紹完四個模式切換所需要符合的升降載率規範，最後就是優先權的問題，當一個模式還沒有執行完，又接到另一個模式的指令，也就是重疊發生時，誰的優先權比較高？ 模式三跟四是臨時觸發跟指派的，優先權當然優於模式一跟二，那最後的問題就是，如果模式三跟四同時觸發，誰的優先權比較高？ 規範如下：",
                "大概就是依據發生先後次序，以及是緊急調度的充電還是放電，來決定優先權，低頻事件比緊急調度的充電優先，而緊急調度的放電則是不受低頻事件影響； 而執行低頻事件時，接獲緊急調度事件，就是執行緊急調度事件。",
                "以上，透過實作這些規則，就可以做出符合規範的E-dReg EMS，剩下就是如何確保執行率跟收益最大化了，POXA EMS都有做喔💪🏻，歡迎與我們聯絡。",
                "邀請大家訂閱POXA Info，除了可以收到第一手訊息外，有些線下活動訊息（如：合格交易者考前衝刺班😎），都是訂閱者優先通知，另外訂閱也是對我們最大的支持，歡迎大家訂閱！ 我們會持續關注未來變化，歡迎各位專家學者、業界專家、用電大戶、發售電業者以及台電能源局長官分享您的看法，每次您寶貴的意見，都能讓POXA離神隊友更近一步💪🏻，歡迎與我們聯絡。"
            ],
            "2": [
                "POXA Energy整理台電電力交易平台公開資料，追蹤每週市場變化的趨勢，完整資料可以參考台電電力交易平台。",
                "本週排名沒有改變，點選看所有排名。"
            ],
            "3": [
                "POXA想藉由監測再生能源的供給跟佔比情況，來了解其對輔助服務市場的影響，預期可以分析：",
                "E-dReg的需求量：E-dReg的需求跟再生能源，尤其是太陽能的佔比息息相關，了解太陽能發電的增長，有助於預測E-dReg的需求量。\n即時跟補充的價格變化：因為國營電廠機組運轉以滿足負載需求為優先，有餘力才會參與輔助服務市場，了解國營供給的情況，有助於預測價格走勢。\n系統頻率的影響：通常再生能源佔比越高，在沒有足夠的儲能下，頻率通常會震盪越大，進而增加調頻服務的執行成本，了解再生能源的供給情況，有助於設計最佳的充放電排程。",
                "本週再生能源佔比平均約12%(風力、太陽能及水力，分別佔比為3.9%、4.8%及3.3%)， 而上週再生能源佔比平均約9%(風力、太陽能及水力，分別佔比為0.2%、7.5%及1.3%)， 再生能源佔比較上週顯著增加，尤其是風力跟水力，尤其是颱風登陸的7/23跟7/25的這三天，風力跟水力發電大幅增加， 太陽能大幅減少，加上颱風假，整體用電負載減少，才會出現再生能源佔比大幅提升的情況。",
                "另外，核三1號機(950MW)運轉執照已於7月27日屆期，依法不可再運轉，所以可以看到核三的發電量只剩2號機的936MW， 而民營豐德燃氣電廠3號機(1100MW)將加入供電，目前台電公告資料狀態為新機組試俥，還沒辦法看到實際供電量， POXA會持續觀測對電網的影響。",
                "本週最高的瞬間滲透率有29.56%，較上週增加，平均滲透率也較上週增加，主要應該是颱風假用電負載減少的關係。",
                "如：裝置容量統計、備轉容量率等，還在建置中...",
                "POXA Energy 擁有自主研發的能源管理系統(Energy Management System，簡稱EMS)與能源資產績效管理服務(Energy Asset Performance Management，簡稱EAPM)。 透過展示對本週市場結清價格與頻率變化的分析與觀察，讓大家可以更了解這些變動對收入及操作策略的影響。",
                "本週頻率分佈與上週接近，但上下界擴大，代表電網狀況較上週不穩定。",
                "電量需求指標代表當儲能最少充放電下的SOC停留位置，本週dReg電量需求指標就上週增加，來到49%，代表電網網往偏電多靠近，是目前最接近50%的一次， 若是想維持SOC=50%，建議位於彈性調整區間時，可採充電策略。",
                "POXA Energy EMS本週預估每日平均放電循環約0.44次，較上週增加，與電網頻率分佈較發散一致。",
                "本週目前一天平均觸發0到1次，但執行時間有變長的趨勢，代表電網狀況較上週不穩定，可能受到颱風影響及E-dReg少了100多MW的影響， 是否會持續造成影響?POXA會持續追蹤最新狀況。"
            ],
            "4": [
                "電力交易市場\n輔助服務市場，https://etp.taipower.com.tw\n輸配電等級儲能專區（可以看目前dReg跟E-dReg申請量）， https://www.taipower.com.tw/tc/page.aspx?mid=6596\n台電公開資料\n機組發電資料、備轉容量、負載預測等資訊，https://www.taipower.com.tw/tc/page.aspx?mid=206\n電價資料\n台電電價資訊，https://www.taipower.com.tw/tc/page.aspx?mid=238\n經濟部能源署電價及費率審議資料揭露中心，https://www3.moeaea.gov.tw/ele102/\n用電大戶（再生能源義務）\n再生能源義務（用電大戶）服務網，https://www.reo.org.tw\n光儲合一\n相關光儲規則、公告、得標廠商及得標量， https://www.moeaea.gov.tw/ECW/populace/home/Home.aspx\n台電太陽光電發電設備結合儲能系統餘電合約(112光儲版)，https://service.taipower.com.tw/powerwheeling/static/file/附件2-太陽光電發電設備結合儲能系統餘電合約(112光儲版)-final.pdf\n台電再生能源購電資料，可用來參考各縣市太陽光電容量因素，https://www.taipower.com.tw/tc/page.aspx?mid=207&cid=165&cchk=a83cd635-a792-4660-9f02-f71d5d925911\n國外電力市場資料來源\n美國電力市場的即時資訊的API及資料下載服務，https://www.gridstatus.io/"
            ]
        }
    }
x = mycol.insert_one(mydata)
print(x.inserted_id)