import uuid
import random
from app.database import SessionLocal, Base, engine
from app.models.category import Category
from app.models.product import Product, ProductImage
from app.schemas.product import ProductStatusEnum

def seed():
    # Tạo các bảng nếu chưa có
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Create Categories
    categories_data = [
        {"name": "Phòng khách", "slug": "phong-khach", "desc": "Nội thất phòng khách sang trọng"},
        {"name": "Phòng ngủ", "slug": "phong-ngu", "desc": "Giường ngủ, tủ quần áo, bàn trang điểm"},
        {"name": "Phòng ăn", "slug": "phong-an", "desc": "Bàn ghế ăn hiện đại"},
        {"name": "Phòng làm việc", "slug": "phong-lam-viec", "desc": "Bàn làm việc, ghế xoay văn phòng"},
    ]
    
    cat_objs = {}
    for c in categories_data:
        cat = db.query(Category).filter(Category.slug == c["slug"]).first()
        if not cat:
            cat = Category(name=c["name"], slug=c["slug"], description=c["desc"])
            db.add(cat)
            db.commit()
            db.refresh(cat)
            print(f"Added category: {cat.name}")
        cat_objs[c["slug"]] = cat
        
    # Create Products
    products_data = [
        # Phòng khách
        {"name": "Sofa Da Thật Nhập Khẩu Ý", "slug": "sofa-da-that-nhap-khau-y", "cat": "phong-khach", "price": 45000000, "material": "Da thật", "color": "Nâu", "stock": 5},
        {"name": "Sofa Nỉ Chữ L Hiện Đại", "slug": "sofa-ni-chu-l-hien-dai", "cat": "phong-khach", "price": 12000000, "material": "Vải nỉ, Khung gỗ", "color": "Xám nhạt", "stock": 10},
        {"name": "Sofa Văng Gỗ Sồi Tân Cổ Điển", "slug": "sofa-vang-go-soi", "cat": "phong-khach", "price": 18500000, "material": "Gỗ sồi, Da công nghiệp", "color": "Trắng gạo", "stock": 8},
        {"name": "Bàn Trà Mặt Đá Nỉ Sintered Stone", "slug": "ban-tra-mat-da-ni", "cat": "phong-khach", "price": 6500000, "material": "Đá ceramic, Thép", "color": "Đen/Trắng", "stock": 15},
        {"name": "Bàn Trà Kính Cường Lực Khung Inox", "slug": "ban-tra-kinh-cuong-luc", "cat": "phong-khach", "price": 3200000, "material": "Kính cường lực, Inox 304", "color": "Trong suốt/Vàng Đồng", "stock": 20},
        {"name": "Kệ Tivi Gỗ Công Nghiệp MDF Lõi Xanh", "slug": "ke-tivi-go-cong-nghiep-mdf", "cat": "phong-khach", "price": 4800000, "material": "MDF chống ẩm, Phủ Melamine", "color": "Vân gỗ sồi", "stock": 12},
        {"name": "Kệ Tivi Treo Tường Decor", "slug": "ke-tivi-treo-tuong-decor", "cat": "phong-khach", "price": 2500000, "material": "Gỗ công nghiệp", "color": "Trắng", "stock": 25},
        
        # Phòng ngủ
        {"name": "Giường Ngủ Gỗ Sồi Nga 1m8", "slug": "giuong-ngu-go-soi-nga-1m8", "cat": "phong-ngu", "price": 9500000, "material": "Gỗ sồi tự nhiên", "color": "Màu gỗ tự nhiên", "stock": 8},
        {"name": "Giường Ngủ Bọc Da Cao Cấp", "slug": "giuong-ngu-boc-da-cao-cap", "cat": "phong-ngu", "price": 15000000, "material": "Da PU, Khung gỗ sồi", "color": "Màu Be", "stock": 5},
        {"name": "Tủ Quần Áo Cửa Lùa Kịch Trần", "slug": "tu-quan-ao-cua-lua-kich-tran", "cat": "phong-ngu", "price": 18000000, "material": "Gỗ MDF chống ẩm", "color": "Gỗ Óc chó", "stock": 10},
        {"name": "Tủ Quần Áo Âm Tường Cánh Kính", "slug": "tu-quan-ao-am-tuong-canh-kinh", "cat": "phong-ngu", "price": 25000000, "material": "Kính cường lực màu xám khói, Khung nhôm", "color": "Tráng gương đen", "stock": 4},
        {"name": "Bàn Trang Điểm Bắc Âu (Nordic Style)", "slug": "ban-trang-diem-bac-au", "cat": "phong-ngu", "price": 3500000, "material": "Gỗ sồi nguyên bản, Gương LED", "color": "Trắng/Sồi nguyên bản", "stock": 12},
        
        # Phòng ăn
        {"name": "Bàn Ăn Gỗ Óc Chó Nguyên Khối Cao Cấp", "slug": "ban-an-go-oc-cho-nguyen-khoi", "cat": "phong-an", "price": 45000000, "material": "Gỗ Óc chó nguyên tấm", "color": "Nâu sậm trầm ấm", "stock": 2},
        {"name": "Bàn Ăn 6 Ghế Hiện Đại Loại Mới", "slug": "ban-an-6-ghe-hien-dai", "cat": "phong-an", "price": 12500000, "material": "Đá ceramic chịu nhiệt, Chân thép sơn tĩnh điện", "color": "Mặt trắng vân mây/Chân đen", "stock": 8},
        {"name": "Bàn Ăn Thông Minh Gấp Gọn Có Bánh Xe", "slug": "ban-an-thong-minh-gap-gon", "cat": "phong-an", "price": 4500000, "material": "Gỗ MDF chống ẩm, cốt xanh", "color": "Trắng/Vân gỗ sáng", "stock": 15},
        {"name": "Ghế Ăn Bọc Nỉ Sang Trọng", "slug": "ghe-an-boc-ni-sang-trong", "cat": "phong-an", "price": 1200000, "material": "Nỉ nhung nhồi mút K43, Chân thép mạ Titan", "color": "Xanh Cổ Vịt", "stock": 50},
        {"name": "Ghế Ăn Gỗ Sồi Tự Nhiên Dây Đan", "slug": "ghe-an-go-soi-tu-nhien-day-dan", "cat": "phong-an", "price": 1800000, "material": "Khung khối gỗ sồi, Mặt ngồi đan dây cói", "color": "Gỗ sồi nguyên bản", "stock": 30},
        
        # Phòng làm việc
        {"name": "Bàn Làm Việc Gỗ Cao Su Nhịp Điệu Chân Sắt Z", "slug": "ban-lam-viec-go-cao-su-chan-sat-z", "cat": "phong-lam-viec", "price": 1500000, "material": "Mặt gỗ cao su tự nhiên ghép thanh cường lực", "color": "Màu gỗ sáng", "stock": 20},
        {"name": "Bàn Gấp Chữ U Chân Sắt Đơn Giản Dành Cho Căn Hộ", "slug": "ban-gap-chu-u-chan-sat", "cat": "phong-lam-viec", "price": 850000, "material": "MDF chống xước, Thép sơn tĩnh điện chống gỉ", "color": "Mặt trắng / Chân đen", "stock": 40},
        {"name": "Ghế Giám Đốc Công Thái Học Ergonomic Cao Cấp", "slug": "ghe-giam-doc-cong-thai-hoc", "cat": "phong-lam-viec", "price": 4500000, "material": "Lưới chịu tải lớn, Nhựa nilon cốt sợi thủy tinh", "color": "Đen toàn bộ", "stock": 10},
        {"name": "Ghế Xoay Lưới Văn Phòng Lưng Cao Rộng Rãi", "slug": "ghe-xoay-luoi-van-phong", "cat": "phong-lam-viec", "price": 1200000, "material": "Lưới nỉ, khung nhựa, chân thép mạ chrome", "color": "Đen thuần", "stock": 50}
    ]

    count = 0
    for p_d in products_data:
        prod = db.query(Product).filter(Product.slug == p_d["slug"]).first()
        if not prod:
            cat_id = cat_objs[p_d["cat"]].id
            new_prod = Product(
                category_id=cat_id,
                name=p_d["name"],
                slug=p_d["slug"],
                description=f"Đây là một sản phẩm nội thất tuyệt vời được khách hàng đánh giá cao. {p_d['name']} được làm từ các chất liệu {p_d['material']} rất phù hợp cho không gian {p_d['cat'].replace('-', ' ')} của bạn. Thiết kế theo tiêu chuẩn hiện đại, độ bền cao qua năm tháng.",
                material=p_d["material"],
                color=p_d["color"],
                price=p_d["price"],
                stock_quantity=p_d["stock"],
                status=ProductStatusEnum.PUBLISHED.value,
                is_featured=random.choice([True, False, False]),
                dimensions="Vui lòng liên hệ để biết kích thước chi tiết"
            )
            db.add(new_prod)
            db.commit()
            db.refresh(new_prod)
            
            # Add some demo image for the product
            img_count = random.randint(2, 4)
            for i in range(img_count):
                db.add(ProductImage(
                    product_id=new_prod.id,
                    image_url=f"https://picsum.photos/seed/{new_prod.slug}-{i}/800/600",
                    is_primary=(i == 0),
                    display_order=i
                ))
            db.commit()
            count += 1
            print(f"Added product: {new_prod.name}")

    print(f"Seed completed. Added {count} new products.")
    db.close()

if __name__ == "__main__":
    seed()
