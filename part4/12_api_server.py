from worker import parse_bao_cao_nang
import time

print("=== GIAO DIỆN KHÁCH HÀNG ===")
print("User: Cho tôi upload cái file 500 trang này!")

start_time = time.time()

task = parse_bao_cao_nang.delay("baocao_500_trang.pdf")

end_time = time.time()

print(f"Server: Đã tiếp nhận đơn hàng, chuyển vào Queue nền. Mã ID của bạn: {task.id}")
print(f"Thời gian phản hồi Server: {(end_time - start_time) * 1000:.2f} ms")

