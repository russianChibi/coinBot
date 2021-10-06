<p>Cách sử dụng:</p>
<h1>6 mode  chính:</h1>
	* release: up lên vps xuất lệnh mua và tự động mua bán sau 1 khoảng thời gian được định sẵn
		-kh: thời gian mỗi nến. nên để mặc định là "1H"
		-ir: INDICATORFILERELEASE: file luư kết quả (/var/www/html/indictor.txt)
		-me: metric thấp nhất. default 16
		-sba: số tiền mặc định mua cho mỗi lệnh. mặc định là 20
	* testStratergy: xuất ra các lệnh bán ra file trong 1 khoảng thời gian nhất định
		-pair: cặt tiền cần kiểm tra. nếu k set thfi sẽ kiểm tra tất cả các cặp tiền của binance
			-pl: vẽ các điểm trên đồ thị. chỉ hỗ trợ khi pair được set
		-kh: thời gian mỗi nến. nên để mặc định là "1H"
		-it: INDICATORFILETEST: file luư kết quả (indicatortest.txt)
		-me: metric thấp nhất. default 16
		-tr: time range for mode test. format: "1 JAN, 2020++1 JAN, 2021"
	* testIndicator: Kiểm tra kết quả của các lệnh mua được xuất ra từ mode "testStratergy". xuất ra số lượng lãi và lỗ theo khoảng % và các lệnh đúng và sai ở 2 file win.txt và lose.txt
		-it: INDICATORFILETEST: file luư kết quả (indicatortest.txt)
		-me: metric thấp nhất. default 16
		-pf: profit mặc định 0.05
		-stl: stoploss mặc định 0.15
		-cy: chu kì lệnh mua bán. mặc định 72 tiếng
	* testAll: Là kết hợp của 2 mode "testStratergy" và "testIndicator":
		-pair: cặt tiền cần kiểm tra. nếu k set thfi sẽ kiểm tra tất cả các cặp tiền của binance
			-pl: vẽ các điểm trên đồ thị. chỉ hỗ trợ khi pair được set
		-kh: thời gian mỗi nến. nên để mặc định là "1H"
		-it: INDICATORFILETEST: file luư kết quả (indicatortest.txt)
		-me: metric thấp nhất. default 16
		-tr: time range for mode test. format: "1 JAN, 2020++1 JAN, 2021"
		-pf: profit mặc định 0.05
		-stl: stoploss mặc định 0.15
		-cy: chu kì lệnh mua bán. mặc định 72 tiếng
	* analysisLog: Phân tích log của chương trình để xuất ra lãi, số lượng các lệnh mua, bán, TBG, chốt lời
		-lp: Đường dẫn chứ thư mục gồm: file indicatorRelease.txt và thư mục log (mặc định là "." vì khi chạy chương trình sẽ tự sinh log ra thư mục hiện tại)
	* panic: bán toàn bộ số token hiện tại (ngoại trừ bnb). Chỉ áp dụng với các token hỗ trợ usdt.
	* analysisLog: xuất báo cáo. tình trạng mua bán.
		-ar: analysis report file path. nếu k có tham số này thì sẽ xuất ra terminal. Sử dụng vòng lặp vô hạn nên dùng để up lên webserver cho dễ nhìn

Sử dụng control.txt để điều khiển luồng chương trình: chỉ cần ghi các lệnh sau vào file thì chương trình sẽ đọc và thực hiện
	stopBuy:  Ngừng mua vào
	stopSell: Ngừng bán ra
	stopFindIndicator: ngừng tìm indicator mới
	sell-BNBUSDT: bán nóng cặp BNBUSDT nếu như cặp này đang được xử lý bởi hàm checkForSell



Ví dụ:
	- Tìm điểm mua trong 1 khoảng thời gian:
		python3 firstCode.py -mo testStrategy -stl 0.20 -pf 0.03 -me 18 -cy 72  -tr  "1 JUL, 2021++9 SEP, 2021"
	- kiểm tra số lệnh thắng trong dong indicator:
		python3 firstCode.py -mo testIndicator -stl 0.20 -pf 0.03 -me 18 -cy 72  -tr  "1 JUL, 2021++9 SEP, 2021"
			- khoảng thời gian 2 tháng từ 1/7-9/9
			- profit ít nhất 3%
			- stoploss 20%
			- metreic > 18
			- chu kì mua bán 72 tiếng
	- Tự tìm điểm mua và kiểm tra số lệnh thắng:
		python3 firstCode.py -mo testAll -stl 0.1 -pf 0.05 -tr  "1 SEP, 2020++9 SEP, 2021"
			- khoảng thời gian 1 tháng từ 2020-2021
			- profit ít nhất 5%
			- stoploss 10%
	python3 firstCode.py -mo testStratergy -pair C98USDT -tr "1 SEP, 2020++9 SEP, 2021" -pl

	python3 firstCode.py -mo analysisLog -lp analysisData



CHIẾN THUẬT TÌM ĐIỂM VÀO: ICHIMOKU CLOUD, RSI, MACD
- mây đỏ (span A < span B)
	- (+2) cắt trong mây
	- (+0) cắt dưới mấy
	- (+3) cắt trên mây
		- (+1 or -12) chưa từng cắt trước đó
	- (-1) conversionLine đã lên quá nhiều (>spanB[i]*1.1) nên trừ điểm
	- (-1) conversionLine chưa chạm tới mây (<spanA[i]*0.9) nên trừ điểm
	- (+1) giá vượt mây
	- kiểm tra độ dài của mây:
		- (+3) dài 20 tiếng
		- (+3) dài 35 tiếng
	- kiểm tra độ sâu của mây:
		- (+3) dảm 10%
		- (+3) dảm 20%

- mây Xanh (span A > span B)
	- cắt trong mây,cắt trên mây
		- (-4) mây xanh đi lên thì giảm điểm
		- (-5) mây xanh  quá 5 tiếng thì giảm điểm
	- (+1) cắt dưới mây
	- (-2) conversionLine đã lên quá nhiều (>spanB[i]*1.1) nên trừ điểm
	- (-2) conversionLine chưa chạm tới mây (<spanA[i]*0.9) nên trừ điểm
	- (+1) giá vượt mây

- laging span
	- (+2) laging span vuot gia
	- (+1) laging span ow giua nen
	- (+1) laging span vuot span A
	- (+1) laging span vuot span B
- (-5) conversionLine di ngang trong 3 tieng
- (-1) kt giá đã tăng nhiều chưa (trên 10%)

- RSI:
	- (-6) rsi qua cao
	- (-6 or +3) kiem tra rsi dang la da tang hay da giam trong 7 tieng
- MACD
	-(-1) macd < macd signal:
		- (-5) giao nhau và khoảng cách ngày càng tăng
	- (+1) macd > macd signal:
		- (+1) macd signal < 0
		- macd và signal cùng > 0:
			- (+1 or -6) kiểm tra xem đã giao nhau từ trước chưa (trong 7 nến)




#####################
stoploss;
	>13%

Chiến thuật mua:
	checkForBuy:
		- lấy toàn bộ cặt tiền trong indicator file mà chwua được mua (không có "xxxxxx")
			- kiểm tra xem có đúng form và giao dịch = usdt hay không
			- Kiểm tra đã có pair này ở trong boughtCoin hay chưa
			- so sánh thời gian hiện tại với thời gian indicator đc tạo ra. nếu lớn hơn 1 nửa của cycle thì huy k mua
			- Kiểm tra số dư usdt hiện tại có thỏa mãn hay k. Nếu k đủ thì cho quay về queue
				- Mua và log ra file

chiến thuật bán:
	checkForSell:
		- Lấy data trong file boughtCoinFile
			- Nếu thời gian vượt quá cycle thì bán nóng
			- Nếu thời gian vượt quá cycle mà k đủ 10 đô thì cũng coi như đã bán
			- Giá mong muốn (hopePrice) lần đầu được set = giá mua *1.03
			- Nếu hiện tại đang lỗ:
				- Nếu đã từng lãi rồi (solanban>0) mà giá về giá mua thì bán toàn bộ
				- lỗ 4% thì mua thêm 25% tổng số tiền
				- lỗ 9% thì mua thêm 25% tổng số tiền
				- lỗ 13% thì cắt lỗ
			- Nếu hiện tại đang lãi:
				- lãi 3% thì bán 30% tổng số coin, giá mong muốn (hopePrice) lên 6%
				- lãi 6% thì bán 30% tổng số coin, giá mong muốn (hopePrice) lên 10%
				- lãi 10% thì bán 50% tổng số coin, giá mong muốn (hopePrice) lên 14%
				- lãi 14% thì bán Hết số coin còn lại
			- Log ra file mua và bán