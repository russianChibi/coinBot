<h1>Cách sử dụng:</h1>
<h2>6 mode  chính:</h2>
	<h3>* release: up lên vps xuất lệnh mua và tự động mua bán sau 1 khoảng thời gian được định sẵn</h3>
		-kh: thời gian mỗi nến. nên để mặc định là "1H"
		-ir: INDICATORFILERELEASE: file luư kết quả (/var/www/html/indictor.txt)
		-me: metric thấp nhất. default 16
		-sba: số tiền mặc định mua cho mỗi lệnh. mặc định là 20
	<h3>* testStratergy: xuất ra các lệnh bán ra file trong 1 khoảng thời gian nhất định</h3>
		-pair: cặt tiền cần kiểm tra. nếu k set thfi sẽ kiểm tra tất cả các cặp tiền của binance
			-pl: vẽ các điểm trên đồ thị. chỉ hỗ trợ khi pair được set
		-kh: thời gian mỗi nến. nên để mặc định là "1H"
		-it: INDICATORFILETEST: file luư kết quả (indicatortest.txt)
		-me: metric thấp nhất. default 16
		-tr: time range for mode test. format: "1 JAN, 2020++1 JAN, 2021"
	<h3>* testIndicator: Kiểm tra kết quả của các lệnh mua được xuất ra từ mode "testStratergy". xuất ra số lượng lãi và lỗ theo khoảng % và các lệnh đúng và sai ở 2 file win.txt và lose.txt<h3>
		-it: INDICATORFILETEST: file luư kết quả (indicatortest.txt)
		-me: metric thấp nhất. default 16
		-pf: profit mặc định 0.05
		-stl: stoploss mặc định 0.15
		-cy: chu kì lệnh mua bán. mặc định 72 tiếng
	<h3>* testAll: Là kết hợp của 2 mode "testStratergy" và "testIndicator":</h3>
		-pair: cặt tiền cần kiểm tra. nếu k set thfi sẽ kiểm tra tất cả các cặp tiền của binance
			-pl: vẽ các điểm trên đồ thị. chỉ hỗ trợ khi pair được set
		-kh: thời gian mỗi nến. nên để mặc định là "1H"
		-it: INDICATORFILETEST: file luư kết quả (indicatortest.txt)
		-me: metric thấp nhất. default 16
		-tr: time range for mode test. format: "1 JAN, 2020++1 JAN, 2021"
		-pf: profit mặc định 0.05
		-stl: stoploss mặc định 0.15
		-cy: chu kì lệnh mua bán. mặc định 72 tiếng
	<h3>* analysisLog: Phân tích log của chương trình để xuất ra lãi, số lượng các lệnh mua, bán, TBG, chốt lời</h3>
		-lp: Đường dẫn chứ thư mục gồm: file indicatorRelease.txt và thư mục log (mặc định là "." vì khi chạy chương trình sẽ tự sinh log ra thư mục hiện tại)
	<h3>* panic: bán toàn bộ số token hiện tại (ngoại trừ bnb). Chỉ áp dụng với các token hỗ trợ usdt.</h3>
	<h3>* analysisLog: xuất báo cáo. tình trạng mua bán.</h3>
		-ar: analysis report file path. nếu k có tham số này thì sẽ xuất ra terminal. Sử dụng vòng lặp vô hạn nên dùng để up lên webserver cho dễ nhìn

<h2>Sử dụng control.txt để điều khiển luồng chương trình: chỉ cần ghi các lệnh sau vào file thì chương trình sẽ đọc và thực hiện</h2>
	<p>stopBuy:  Ngừng mua vào</p>
	<p>stopSell: Ngừng bán ra</p>
	<p>stopFindIndicator: ngừng tìm indicator mới</p>
	<p>sell-BNBUSDT: bán nóng cặp BNBUSDT nếu như cặp này đang được xử lý bởi hàm checkForSell</p>


<h2>Ví dụ:</h2>
	<h3>- Tìm điểm mua trong 1 khoảng thời gian:</h3>
		python3 firstCode.py -mo testStrategy -stl 0.20 -pf 0.03 -me 18 -cy 72  -tr  "1 JUL, 2021++9 SEP, 2021"
	<h3>- Kiểm tra số lệnh thắng trong dong indicator:</h3>
		python3 firstCode.py -mo testIndicator -stl 0.20 -pf 0.03 -me 18 -cy 72  -tr  "1 JUL, 2021++9 SEP, 2021"
			<p>- khoảng thời gian 2 tháng từ 1/7-9/9</p>
			<p>- profit ít nhất 3%</p>
			<p>- stoploss 20%</p>
			<p>- metreic > 18</p>
			<p>- chu kì mua bán 72 tiếng</p>
	<h3>- Tự tìm điểm mua và kiểm tra số lệnh thắng:</h3>
		python3 firstCode.py -mo testAll -stl 0.1 -pf 0.05 -tr  "1 SEP, 2020++9 SEP, 2021"
			<p>- khoảng thời gian 1 tháng từ 2020-2021</p>
			<p>- profit ít nhất 5%</p>
			<p>- stoploss 10%</p>