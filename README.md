# Citation Network
Parse citation data of collaboration network
(text below is in Vietnamese)

**citationnetwork** là chương trình Python3, nhằm giúp phân tích dữ liệu xuất bản khoa học và thống kê các trích dẫn của những nhóm cộng tác trong việc xuất bản các ấn phẩm khoa học.

# Cách dùng công cụ Citation Network:
## Chuẩn bị dữ liệu:
Export dữ liệu citations từ Scopus, với các thông tin: tên bài báo, tên tác giả, tên tác giả kèm affiliations, tên tạp chí, tên nhà xuất bản, năm xuất bản, địa chỉ DOI, danh sách các trích dẫn (references) trong bài.
Đặt tất cả các file dữ liệu đầu vào ở thư mục con có tên **scopus_data**.

## Chạy chương trình từng bước:

### Chạy file *get_sources.py* (trên nền tảng Python 3), để liệt kê tên tất cả các tạp chí, hội nghị, nó sẽ đọc các file .csv trong cơ sở dữ liệu ở thư mục scopus_data và xuất ra file ***list_sources.csv***.
Sau khi file list_sources.csv được tạo ra tự động, người dùng có thể mở file này bằng Excel hay OpenOffice để thêm thông tin riêng của mình: Trong file list_sources.csv có cột cuối cùng là Rating, để người sử dụng tự nhập đánh giá của mình về tạp chí đó (ví dụ có thể ghi chú đó là tạp chí "Top"/"Good"/"Ok"/"Bad"/"Avoid" hay cũng có thể điền một số vào đó).

Nếu người dùng đã chuẩn bị file input_net_authors.txt (xem ở dưới) thì chạy file *get_sources_net.py* để chương trình chỉ lọc ra các tạp chí mà các tác giả liên quan có xuất bản ở đó, file output là list_sources_net.csv, danh sách các tạp chí trong này sẽ ít hơn nhiều so với list_sources.csv khi chạy phân tích toàn bộ các tạp chí. Sau đó, sửa file list_sources_net.csv đẻ thêm dữ liệu Rating cho tạp chí, rồi đổi tên file đó thành list_sources.csv để dùng ở bước tiếp theo.


### Chạy file *get_authors.py* nó sẽ đọc tất cả các file trong **scopus_data** và xuất ra file **list_all_authors.csv**
Cấu trúc của **list_all_authors.csv** có các cột:
1. Tên tác giả
2. Số lượng affiliations trong các bài của tác giả này
3. Các affiliations của tác giả này (phân cách bằng dấu chấm phẩy)

### Chạy file *get_papers.py*, nó sẽ đọc tất cả các file trong **scopus_data** và file list_sources.csv (để lấy nhãn Rating của tạp chí vào làm Rating cho bài báo), để xuất ra file **list_papers.csv**
Cấu trúc của **list_papers.csv** có các cột:
1. ID (số thứ tự trong danh sách)
2. Tên bài báo (nếu có nhiều bài báo trùng tên, hoặc một bài được liệt kê ở nhiều chỗ, thì chỉ lọc giữ lại một bài)
3. Tên các tác giả (TODO: xét trường hợp một tác giả có thể được liệt kê với cách viết tên khác nhau)
4. Tên tạp chí
5. Tên nhà xuất bản
6. Năm xuất bản
7. Địa chỉ DOI
8. Rating (kế thừa từ Rating của tạp chí do người dùng đã đánh giá)
  
### Chạy file *get_references.py*, nó sẽ đọc một lần nữa tất cả các file trong **scopus_data** cùng với file **list_papers.csv** và xuất ra file **list_references.csv**.
Cấu trúc của **list_references.csv** có các cột:
1. ID (trùng với ID trong file list_papers.csv)
2. Tổng số references của bài này
3. Số lượng references nằm ngoài danh mục các bài đã thu thập được trong file list_papers.csv
4. Số lượng references nằm trong danh mục các bài đã thu thập được trong file list_papers.csv
5. Số lượng references trong danh mục ở file list_papers.csv mà có trùng ít nhất 1 tác giả với bài này (self cite)
6. Danh sách các bài nằm trong list_papers.csv mà bài này đã cite (liệt kê chuỗi các ID, ngăn cách bằng dấu phẩy, e.g. 2,15,40)
và các cột còn lại trong file list_papers.csv (từ Tên bài báo, đến Địa chỉ DOI)
7. Rating của bài này
8... Các cột thống kê cho biết số lượng bài trong danh sách references thuộc các nhóm Rating nào (mỗi nhóm là ở một cột, nhóm mặc định là để trống, nếu không có thông tin Rating của tạp chí chứa reference)
  
### Chạy file *get_citations.csv*, nó sẽ đọc file **list_references.csv** và xuất ra file **list_citations.csv**.
Cấu trúc của list_citations.csv có các cột:
1. ID (trùng với ID trong file list_papers.csv)
2. Tổng số citations của bài này, xét trong phạm vi danh mục các bài đã thu thập được trong file list_papers.csv
3. Danh sách các bài nằm trong list_papers.csv đã cite bài này (liệt kê chuỗi các ID, ngăn cách bằng dấu phẩy, e.g. 6,8,9)
và các cột còn lại trong file list_papers.csv (từ Tên bài báo, đến Địa chỉ DOI)
  
### *Tạo* một file ***input_net_authors.txt*** để liệt kê nhóm tác giả cần phân tích collaboration network, mà mỗi dòng là tên của một tác giả.

### Chạy file *count_references.py*, nó sẽ đọc file **list_references.csv** và file ***input_net_authors.txt*** rồi xuất ra file **references_net.csv**
Cấu trúc của ***references_net.csv*** có các cột (liệt kê theo từng tác giả):
1. ID (ứng với số hàng ghi tên tác giả trong file input_net_authors.txt)
2. Tên tác giả
3. Tổng số bài của tác giả này trong danh mục đã thu thập ở file list_papers.csv
4. Số lượng các bài của tác giả này mà có cite bài của ít nhất một người trong danh sách tác giả được liệt kê ở input_net_authors.txt
5. Số lượng các bài của tác giả này nhận được citations từ bất kỳ tác giả nào khác trong danh sách ở input_net_authors.txt (kể cả họ là đồng tác giả với mình)
6. Tổng số references trong các bài của tác giả này
7. Số lượng references trong các bài của tác giả này do một trong những người ở input_net_authors.txt là đồng tác giả (self cite + ring cite)
8. Tổng số citations mà các bài của tác giả này nhận được từ bài của những người nằm trong danh sách input_net_authors.txt
9. Các cột cho biết số references (hay citations) mà các bài của tác giả này dành cho từng người trong danh sách tác giả ở input_net_authors.txt (khi mở trong Excel, phần các cột này tạo thành ma trận vuông).
  
## Sử dụng kết quả:

Chương trình này chưa có tính năng vẽ đồ thị kết nối, mà chỉ xuất kết quả ra các file .csv (comma-separated values).

Đọc file **list_all_authors.csv**: mở bằng Microsoft Excel hoặc OpenOffice.Org Calc, để import file CSV này thành bảng tính. Xem ở cột số lượng các affiliations, có thể sắp xếp lại theo thứ tự giảm dần ở cột đó, nếu người nào có nhiều affiliations ở những nơi khác nhau thì là họ cộng tác với nhiều nơi.

File **list_papers.csv**: file này chỉ là kết quả trung gian.

Đọc file **list_references.csv**: có thể sắp xếp lại theo cột Number of self-cited references (hoặc tạo cột tính tỷ lệ Number of self-cited references/Number of references) để biết bài báo nào có số lượng tự trích dẫn cao. Đọc tên tác giả các bài báo có số lượng tự trích dẫn cao, để tăng cường dữ liệu (lấy từ Scopus) về những bài liên quan đến người đó, và làm phân tích lại.

Đọc file **list_citations.csv**: cách dùng tương tự như **list_references.csv**

Đọc file **references_net.csv**: các con số quan trọng nằm ở cột Number of references to network authors (self cite + ring cite), xét trong tương quan với Total number of references in author' papers. Số liệu ở cột Number of citations from network authors cũng đáng quan tâm, có thể  so sánh con số đó với tổng số citations mà tác giả nhận được (xem trên trang Scopus) để biết tác giả có nhận được nhiều citations từ những người ở ngoài collaboration network hay không.

Người phân tích có thể chỉnh lại danh sách trong file input_net_authors.txt để thay đổi phạm vi thống kê (tăng, giảm người trong collaboration network), rồi chạy lại file *count_references.py* và khảo sát kết quả ở **references_net.csv** (lặp lại khảo sát nhiều vòng, với hy vọng kết quả rõ ràng dần).
  
## Các công cụ bổ sung:

### Merge dữ liệu tải về từ Scopus:
Khi chạy file merge_scopus_data.py, nó sẽ đọc tất cả các file trong thư mục scopus_data, rồi xuất ra một file toàn bộ dữ liệu có tên ***all_database.csv***, tự loại bỏ những dòng dữ liệu trùng lắp trong các file. Công cụ này tiện dụng để tạo ra file dữ liệu duy nhất dùng cho một chương trình khác, như VOSviewer.