import random

from app.database import Base, SessionLocal, engine
from app.models.product import Product, ProductImage
from app.models.product_category import ProductCategory
from app.models.product_collection import ProductCollection
from app.models.product_color import ProductColor
from app.models.product_material import ProductMaterial
from app.models.product_type import ProductType
from app.schemas.product import ProductStatusEnum


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # ── 1. Product Categories ─────────────────────────────────────────────────
    categories_data = [
        {
            "name": "Phòng khách",
            "slug": "phong-khach",
            "desc": "Nội thất phòng khách sang trọng",
        },
        {
            "name": "Phòng ngủ",
            "slug": "phong-ngu",
            "desc": "Giường ngủ, tủ quần áo, bàn trang điểm",
        },
        {"name": "Phòng ăn", "slug": "phong-an", "desc": "Bàn ghế ăn hiện đại"},
        {
            "name": "Phòng làm việc",
            "slug": "phong-lam-viec",
            "desc": "Bàn làm việc, ghế xoay văn phòng",
        },
    ]
    cat_objs = {}
    for c in categories_data:
        obj = (
            db.query(ProductCategory).filter(ProductCategory.slug == c["slug"]).first()
        )
        if not obj:
            obj = ProductCategory(name=c["name"], slug=c["slug"], description=c["desc"])
            db.add(obj)
            db.commit()
            db.refresh(obj)
            print(f"Added category: {obj.name}")
        cat_objs[c["slug"]] = obj

    # ── 2. Product Types ──────────────────────────────────────────────────────
    product_types_data = [
        {"name": "Sofa", "slug": "sofa", "desc": "Các loại sofa phòng khách"},
        {
            "name": "Bàn trà",
            "slug": "ban-tra",
            "desc": "Bàn trà, bàn coffee decor phòng khách",
        },
        {"name": "Kệ tivi", "slug": "ke-tivi", "desc": "Kệ tivi, tủ tivi các loại"},
        {
            "name": "Giường ngủ",
            "slug": "giuong-ngu",
            "desc": "Giường ngủ đơn, đôi, cỡ lớn",
        },
        {
            "name": "Tủ quần áo",
            "slug": "tu-quan-ao",
            "desc": "Tủ đựng quần áo, tủ âm tường",
        },
        {
            "name": "Bàn trang điểm",
            "slug": "ban-trang-diem",
            "desc": "Bàn trang điểm, bàn phấn kèm gương",
        },
        {"name": "Bàn ăn", "slug": "ban-an", "desc": "Bàn ăn gia đình các kích cỡ"},
        {"name": "Ghế ăn", "slug": "ghe-an", "desc": "Ghế ăn rời, bộ ghế ăn"},
        {
            "name": "Bàn làm việc",
            "slug": "ban-lam-viec",
            "desc": "Bàn làm việc, bàn học, bàn máy tính",
        },
        {
            "name": "Ghế văn phòng",
            "slug": "ghe-van-phong",
            "desc": "Ghế xoay, ghế công thái học",
        },
    ]
    type_objs = {}
    for t in product_types_data:
        obj = db.query(ProductType).filter(ProductType.slug == t["slug"]).first()
        if not obj:
            obj = ProductType(name=t["name"], slug=t["slug"], description=t["desc"])
            db.add(obj)
            db.commit()
            db.refresh(obj)
            print(f"Added product type: {obj.name}")
        type_objs[t["slug"]] = obj

    # ── 3. Product Colors (master) ────────────────────────────────────────────
    colors_data = [
        {"name": "Nâu sậm", "hex_code": "#5C3317"},
        {"name": "Đen huyền", "hex_code": "#1A1A1A"},
        {"name": "Be sữa", "hex_code": "#F5F0E8"},
        {"name": "Xám nhạt", "hex_code": "#C8C8C8"},
        {"name": "Xanh rêu", "hex_code": "#4A5E3A"},
        {"name": "Kem vàng", "hex_code": "#F0E4C2"},
        {"name": "Trắng gạo", "hex_code": "#F5F0E0"},
        {"name": "Xanh cổ vịt", "hex_code": "#3D7A8A"},
        {"name": "Đen vân đá", "hex_code": "#2B2B2B"},
        {"name": "Trắng vân mây", "hex_code": "#F0EEE8"},
        {"name": "Trong suốt/Vàng đồng", "hex_code": "#B8860B"},
        {"name": "Trong suốt/Bạc", "hex_code": "#C0C0C0"},
        {"name": "Vân gỗ sồi", "hex_code": "#C8A87A"},
        {"name": "Trắng", "hex_code": "#FFFFFF"},
        {"name": "Gỗ tự nhiên", "hex_code": "#C4A35A"},
        {"name": "Nâu walnut", "hex_code": "#5C3A1E"},
        {"name": "Màu be", "hex_code": "#D2B48C"},
        {"name": "Xám xi măng", "hex_code": "#808080"},
        {"name": "Gỗ Óc chó", "hex_code": "#4A2C0A"},
        {"name": "Trắng ngà", "hex_code": "#FFFFF0"},
        {"name": "Tráng gương đen", "hex_code": "#1C1C1C"},
        {"name": "Kính xám khói", "hex_code": "#708090"},
        {"name": "Sồi sáng", "hex_code": "#D4AA70"},
        {"name": "Nâu sậm trầm", "hex_code": "#3B1F0C"},
        {"name": "Nâu trung tính", "hex_code": "#6B3A2A"},
        {"name": "Gỗ sồi nhuộm đen", "hex_code": "#2C2C2C"},
        {"name": "Đen/Chân vàng", "hex_code": "#B8860B"},
        {"name": "Đen", "hex_code": "#222222"},
        {"name": "Xám xi", "hex_code": "#555555"},
    ]
    color_objs = {}
    for c in colors_data:
        obj = db.query(ProductColor).filter(ProductColor.name == c["name"]).first()
        if not obj:
            obj = ProductColor(name=c["name"], hex_code=c["hex_code"])
            db.add(obj)
            db.commit()
            db.refresh(obj)
            print(f"Added color: {obj.name}")
        color_objs[c["name"]] = obj

    # ── 4. Product Materials (master) ─────────────────────────────────────────
    materials_data = [
        {
            "name": "Da thật Ý nhập khẩu",
            "image_url": "https://picsum.photos/seed/leather-italy/120/120",
        },
        {
            "name": "Khung gỗ sồi nguyên tấm",
            "image_url": "https://picsum.photos/seed/oak-frame/120/120",
        },
        {
            "name": "Vải nỉ cao cấp",
            "image_url": "https://picsum.photos/seed/fabric-ni/120/120",
        },
        {"name": "Khung gỗ công nghiệp", "image_url": None},
        {
            "name": "Gỗ sồi tự nhiên",
            "image_url": "https://picsum.photos/seed/oak-wood/120/120",
        },
        {
            "name": "Da công nghiệp PU",
            "image_url": "https://picsum.photos/seed/pu-leather/120/120",
        },
        {
            "name": "Đá Sintered Stone ceramic",
            "image_url": "https://picsum.photos/seed/sintered-stone/120/120",
        },
        {
            "name": "Chân thép sơn tĩnh điện",
            "image_url": "https://picsum.photos/seed/steel-leg/120/120",
        },
        {
            "name": "Kính cường lực 10mm",
            "image_url": "https://picsum.photos/seed/tempered-glass/120/120",
        },
        {"name": "Khung Inox 304", "image_url": None},
        {
            "name": "MDF chống ẩm lõi xanh",
            "image_url": "https://picsum.photos/seed/mdf-green/120/120",
        },
        {"name": "Phủ bề mặt Melamine", "image_url": None},
        {
            "name": "Gỗ sồi Nga nhập khẩu",
            "image_url": "https://picsum.photos/seed/oak-russian/120/120",
        },
        {
            "name": "Da PU cao cấp",
            "image_url": "https://picsum.photos/seed/pu-bed/120/120",
        },
        {
            "name": "Gỗ MDF chống ẩm 18mm",
            "image_url": "https://picsum.photos/seed/mdf-wardrobe/120/120",
        },
        {
            "name": "Mặt phủ vân Óc chó",
            "image_url": "https://picsum.photos/seed/walnut-surface/120/120",
        },
        {
            "name": "Kính cường lực màu xám khói",
            "image_url": "https://picsum.photos/seed/smoked-glass/120/120",
        },
        {"name": "Khung nhôm anodized", "image_url": None},
        {
            "name": "Gỗ sồi nguyên bản",
            "image_url": "https://picsum.photos/seed/oak-vanity/120/120",
        },
        {"name": "Gương LED viền mỏng", "image_url": None},
        {
            "name": "Gỗ Óc chó nguyên tấm slab",
            "image_url": "https://picsum.photos/seed/walnut-slab/120/120",
        },
        {
            "name": "Đá ceramic chịu nhiệt",
            "image_url": "https://picsum.photos/seed/ceramic-table/120/120",
        },
        {
            "name": "Gỗ MDF gấp gọn",
            "image_url": "https://picsum.photos/seed/mdf-foldable/120/120",
        },
        {
            "name": "Nỉ nhung nhồi mút K43",
            "image_url": "https://picsum.photos/seed/velvet-chair/120/120",
        },
        {"name": "Chân thép mạ Titan", "image_url": None},
        {
            "name": "Khung gỗ sồi khối nguyên",
            "image_url": "https://picsum.photos/seed/oak-chair/120/120",
        },
        {
            "name": "Đan dây cói tự nhiên",
            "image_url": "https://picsum.photos/seed/rattan-weave/120/120",
        },
        {
            "name": "Mặt gỗ cao su ghép thanh",
            "image_url": "https://picsum.photos/seed/rubber-wood/120/120",
        },
        {"name": "Chân sắt sơn tĩnh điện", "image_url": None},
        {"name": "MDF chống xước 15mm", "image_url": None},
        {"name": "Thép sơn tĩnh điện chống gỉ", "image_url": None},
        {
            "name": "Lưới thoáng khí chịu tải",
            "image_url": "https://picsum.photos/seed/mesh-chair/120/120",
        },
        {"name": "Nhựa nilon cốt sợi thủy tinh", "image_url": None},
        {"name": "Chân nylon xoay 360°", "image_url": None},
        {
            "name": "Lưới nỉ thoáng khí",
            "image_url": "https://picsum.photos/seed/mesh-office/120/120",
        },
        {"name": "Khung nhựa ABS", "image_url": None},
        {"name": "Chân thép mạ chrome", "image_url": None},
    ]
    mat_objs = {}
    for m in materials_data:
        obj = (
            db.query(ProductMaterial).filter(ProductMaterial.name == m["name"]).first()
        )
        if not obj:
            obj = ProductMaterial(name=m["name"], image_url=m["image_url"])
            db.add(obj)
            db.commit()
            db.refresh(obj)
            print(f"Added material: {obj.name}")
        mat_objs[m["name"]] = obj

    # ── 5. Products ───────────────────────────────────────────────────────────
    # colors/materials = list of names referencing master objects above
    products_data = [
        # Phòng khách – Sofa
        {
            "name": "Sofa Da Thật Nhập Khẩu Ý",
            "slug": "sofa-da-that-nhap-khau-y",
            "cat": "phong-khach",
            "type": "sofa",
            "price": 45_000_000,
            "stock": 5,
            "colors": ["Nâu sậm", "Đen huyền", "Be sữa"],
            "materials": ["Da thật Ý nhập khẩu", "Khung gỗ sồi nguyên tấm"],
        },
        {
            "name": "Sofa Nỉ Chữ L Hiện Đại",
            "slug": "sofa-ni-chu-l-hien-dai",
            "cat": "phong-khach",
            "type": "sofa",
            "price": 12_000_000,
            "stock": 10,
            "colors": ["Xám nhạt", "Xanh rêu", "Kem vàng"],
            "materials": ["Vải nỉ cao cấp", "Khung gỗ công nghiệp"],
        },
        {
            "name": "Sofa Văng Gỗ Sồi Tân Cổ Điển",
            "slug": "sofa-vang-go-soi",
            "cat": "phong-khach",
            "type": "sofa",
            "price": 18_500_000,
            "stock": 8,
            "colors": ["Trắng gạo", "Xanh cổ vịt"],
            "materials": ["Gỗ sồi tự nhiên", "Da công nghiệp PU"],
        },
        # Phòng khách – Bàn trà
        {
            "name": "Bàn Trà Mặt Đá Sintered Stone",
            "slug": "ban-tra-mat-da-ni",
            "cat": "phong-khach",
            "type": "ban-tra",
            "price": 6_500_000,
            "stock": 15,
            "colors": ["Đen vân đá", "Trắng vân mây"],
            "materials": ["Đá Sintered Stone ceramic", "Chân thép sơn tĩnh điện"],
        },
        {
            "name": "Bàn Trà Kính Cường Lực Khung Inox",
            "slug": "ban-tra-kinh-cuong-luc",
            "cat": "phong-khach",
            "type": "ban-tra",
            "price": 3_200_000,
            "stock": 20,
            "colors": ["Trong suốt/Vàng đồng", "Trong suốt/Bạc"],
            "materials": ["Kính cường lực 10mm", "Khung Inox 304"],
        },
        # Phòng khách – Kệ tivi
        {
            "name": "Kệ Tivi Gỗ MDF Lõi Xanh",
            "slug": "ke-tivi-go-cong-nghiep-mdf",
            "cat": "phong-khach",
            "type": "ke-tivi",
            "price": 4_800_000,
            "stock": 12,
            "colors": ["Vân gỗ sồi", "Trắng"],
            "materials": ["MDF chống ẩm lõi xanh", "Phủ bề mặt Melamine"],
        },
        {
            "name": "Kệ Tivi Treo Tường Decor",
            "slug": "ke-tivi-treo-tuong-decor",
            "cat": "phong-khach",
            "type": "ke-tivi",
            "price": 2_500_000,
            "stock": 25,
            "colors": ["Trắng", "Đen huyền"],
            "materials": ["Khung gỗ công nghiệp"],
        },
        # Phòng ngủ – Giường
        {
            "name": "Giường Ngủ Gỗ Sồi Nga 1m8",
            "slug": "giuong-ngu-go-soi-nga-1m8",
            "cat": "phong-ngu",
            "type": "giuong-ngu",
            "price": 9_500_000,
            "stock": 8,
            "colors": ["Gỗ tự nhiên", "Nâu walnut"],
            "materials": ["Gỗ sồi Nga nhập khẩu"],
        },
        {
            "name": "Giường Ngủ Bọc Da Cao Cấp",
            "slug": "giuong-ngu-boc-da-cao-cap",
            "cat": "phong-ngu",
            "type": "giuong-ngu",
            "price": 15_000_000,
            "stock": 5,
            "colors": ["Màu be", "Xám xi măng"],
            "materials": ["Da PU cao cấp", "Khung gỗ sồi nguyên tấm"],
        },
        # Phòng ngủ – Tủ quần áo
        {
            "name": "Tủ Quần Áo Cửa Lùa Kịch Trần",
            "slug": "tu-quan-ao-cua-lua-kich-tran",
            "cat": "phong-ngu",
            "type": "tu-quan-ao",
            "price": 18_000_000,
            "stock": 10,
            "colors": ["Gỗ Óc chó", "Trắng ngà"],
            "materials": ["Gỗ MDF chống ẩm 18mm", "Mặt phủ vân Óc chó"],
        },
        {
            "name": "Tủ Quần Áo Âm Tường Cánh Kính",
            "slug": "tu-quan-ao-am-tuong-canh-kinh",
            "cat": "phong-ngu",
            "type": "tu-quan-ao",
            "price": 25_000_000,
            "stock": 4,
            "colors": ["Tráng gương đen", "Kính xám khói"],
            "materials": ["Kính cường lực màu xám khói", "Khung nhôm anodized"],
        },
        # Phòng ngủ – Bàn trang điểm
        {
            "name": "Bàn Trang Điểm Nordic Style",
            "slug": "ban-trang-diem-bac-au",
            "cat": "phong-ngu",
            "type": "ban-trang-diem",
            "price": 3_500_000,
            "stock": 12,
            "colors": ["Trắng", "Sồi sáng"],
            "materials": ["Gỗ sồi nguyên bản", "Gương LED viền mỏng"],
        },
        # Phòng ăn – Bàn ăn
        {
            "name": "Bàn Ăn Gỗ Óc Chó Nguyên Khối",
            "slug": "ban-an-go-oc-cho-nguyen-khoi",
            "cat": "phong-an",
            "type": "ban-an",
            "price": 45_000_000,
            "stock": 2,
            "colors": ["Nâu sậm trầm", "Nâu trung tính"],
            "materials": ["Gỗ Óc chó nguyên tấm slab"],
        },
        {
            "name": "Bàn Ăn 6 Ghế Đá Ceramic Hiện Đại",
            "slug": "ban-an-6-ghe-hien-dai",
            "cat": "phong-an",
            "type": "ban-an",
            "price": 12_500_000,
            "stock": 8,
            "colors": ["Trắng vân mây", "Đen vân đá"],
            "materials": ["Đá ceramic chịu nhiệt", "Chân thép sơn tĩnh điện"],
        },
        {
            "name": "Bàn Ăn Thông Minh Gấp Gọn",
            "slug": "ban-an-thong-minh-gap-gon",
            "cat": "phong-an",
            "type": "ban-an",
            "price": 4_500_000,
            "stock": 15,
            "colors": ["Trắng", "Vân gỗ sồi"],
            "materials": ["Gỗ MDF gấp gọn"],
        },
        # Phòng ăn – Ghế ăn
        {
            "name": "Ghế Ăn Bọc Nỉ Sang Trọng",
            "slug": "ghe-an-boc-ni-sang-trong",
            "cat": "phong-an",
            "type": "ghe-an",
            "price": 1_200_000,
            "stock": 50,
            "colors": ["Xanh cổ vịt", "Xám nhạt", "Kem vàng"],
            "materials": ["Nỉ nhung nhồi mút K43", "Chân thép mạ Titan"],
        },
        {
            "name": "Ghế Ăn Gỗ Sồi Dây Đan",
            "slug": "ghe-an-go-soi-tu-nhien-day-dan",
            "cat": "phong-an",
            "type": "ghe-an",
            "price": 1_800_000,
            "stock": 30,
            "colors": ["Gỗ tự nhiên", "Gỗ sồi nhuộm đen"],
            "materials": ["Khung gỗ sồi khối nguyên", "Đan dây cói tự nhiên"],
        },
        # Phòng làm việc – Bàn
        {
            "name": "Bàn Làm Việc Gỗ Cao Su Chân Sắt Z",
            "slug": "ban-lam-viec-go-cao-su-chan-sat-z",
            "cat": "phong-lam-viec",
            "type": "ban-lam-viec",
            "price": 1_500_000,
            "stock": 20,
            "colors": ["Gỗ tự nhiên", "Nâu walnut"],
            "materials": ["Mặt gỗ cao su ghép thanh", "Chân sắt sơn tĩnh điện"],
        },
        {
            "name": "Bàn Gấp Chữ U Chân Sắt Căn Hộ",
            "slug": "ban-gap-chu-u-chan-sat",
            "cat": "phong-lam-viec",
            "type": "ban-lam-viec",
            "price": 850_000,
            "stock": 40,
            "colors": ["Trắng", "Vân gỗ sồi"],
            "materials": ["MDF chống xước 15mm", "Thép sơn tĩnh điện chống gỉ"],
        },
        # Phòng làm việc – Ghế
        {
            "name": "Ghế Giám Đốc Ergonomic Cao Cấp",
            "slug": "ghe-giam-doc-cong-thai-hoc",
            "cat": "phong-lam-viec",
            "type": "ghe-van-phong",
            "price": 4_500_000,
            "stock": 10,
            "colors": ["Đen", "Xám xi"],
            "materials": [
                "Lưới thoáng khí chịu tải",
                "Nhựa nilon cốt sợi thủy tinh",
                "Chân nylon xoay 360°",
            ],
        },
        {
            "name": "Ghế Xoay Lưới Văn Phòng Lưng Cao",
            "slug": "ghe-xoay-luoi-van-phong",
            "cat": "phong-lam-viec",
            "type": "ghe-van-phong",
            "price": 1_200_000,
            "stock": 50,
            "colors": ["Đen"],
            "materials": [
                "Lưới nỉ thoáng khí",
                "Khung nhựa ABS",
                "Chân thép mạ chrome",
            ],
        },
    ]

    # ── 5. Products ───────────────────────────────────────────────────────────
    count = 0
    for p_d in products_data:
        prod = db.query(Product).filter(Product.slug == p_d["slug"]).first()
        if not prod:
            cat_id = cat_objs[p_d["cat"]].id
            type_id = type_objs[p_d["type"]].id
            mat_names = ", ".join(p_d["materials"])

            new_prod = Product(
                category_id=cat_id,
                product_type_id=type_id,
                name=p_d["name"],
                slug=p_d["slug"],
                description=(
                    f"Đây là một sản phẩm nội thất tuyệt vời được khách hàng đánh giá cao. "
                    f"{p_d['name']} được làm từ {mat_names}, "
                    f"rất phù hợp cho không gian {p_d['cat'].replace('-', ' ')} của bạn. "
                    f"Thiết kế theo tiêu chuẩn hiện đại, độ bền cao qua năm tháng."
                ),
                price=p_d["price"],
                stock_quantity=p_d["stock"],
                status=ProductStatusEnum.PUBLISHED.value,
                is_featured=random.choice([True, False, False]),
                dimensions="Vui lòng liên hệ để biết kích thước chi tiết",
                colors=[color_objs[name] for name in p_d["colors"]],
                materials=[mat_objs[name] for name in p_d["materials"]],
            )
            db.add(new_prod)
            db.flush()

            img_count = random.randint(2, 4)
            for i in range(img_count):
                db.add(
                    ProductImage(
                        product_id=new_prod.id,
                        image_url=f"https://picsum.photos/seed/{new_prod.slug}-{i}/800/600",
                        is_primary=(i == 0),
                        display_order=i,
                    )
                )

            db.commit()
            count += 1
            print(f"Added product: {new_prod.name}")

    # ── 6. Product Collections ────────────────────────────────────────────────
    collections_data = [
        {
            "name": "Phong Cách Scandinavian",
            "slug": "scandinavian",
            "desc": "Thiết kế tối giản Bắc Âu — gỗ sáng, đường nét gọn ghẽ, không gian thoáng đãng.",
            "image_url": "https://picsum.photos/seed/collection-scandinavian/800/500",
            "is_featured": True,
            "products": [
                "sofa-ni-chu-l-hien-dai",
                "ban-trang-diem-bac-au",
                "ban-gap-chu-u-chan-sat",
                "ghe-an-go-soi-tu-nhien-day-dan",
            ],
        },
        {
            "name": "Phong Cách Industrial",
            "slug": "industrial",
            "desc": "Vật liệu thô — thép, gỗ nguyên khối, tường gạch. Phong cách công xưởng đô thị.",
            "image_url": "https://picsum.photos/seed/collection-industrial/800/500",
            "is_featured": True,
            "products": [
                "ban-tra-kinh-cuong-luc",
                "ban-lam-viec-go-cao-su-chan-sat-z",
                "ghe-xoay-luoi-van-phong",
                "ke-tivi-treo-tuong-decor",
            ],
        },
        {
            "name": "Luxury & Classic",
            "slug": "luxury-classic",
            "desc": "Nội thất cao cấp — da thật, gỗ tự nhiên nhập khẩu, đường nét tân cổ điển.",
            "image_url": "https://picsum.photos/seed/collection-luxury/800/500",
            "is_featured": True,
            "products": [
                "sofa-da-that-nhap-khau-y",
                "giuong-ngu-boc-da-cao-cap",
                "ban-an-go-oc-cho-nguyen-khoi",
                "tu-quan-ao-am-tuong-canh-kinh",
            ],
        },
        {
            "name": "Home Office 2025",
            "slug": "home-office-2025",
            "desc": "Bộ sưu tập không gian làm việc tại nhà — ergonomic, gọn gàng, hiệu quả.",
            "image_url": "https://picsum.photos/seed/collection-homeoffice/800/500",
            "is_featured": False,
            "products": [
                "ban-lam-viec-go-cao-su-chan-sat-z",
                "ghe-giam-doc-cong-thai-hoc",
                "ban-gap-chu-u-chan-sat",
                "ghe-xoay-luoi-van-phong",
            ],
        },
        {
            "name": "Phòng Ngủ Hoàng Gia",
            "slug": "phong-ngu-hoang-gia",
            "desc": "Giường, tủ, bàn trang điểm — combo phòng ngủ hoàn chỉnh sang trọng.",
            "image_url": "https://picsum.photos/seed/collection-bedroom/800/500",
            "is_featured": False,
            "products": [
                "giuong-ngu-go-soi-nga-1m8",
                "giuong-ngu-boc-da-cao-cap",
                "tu-quan-ao-cua-lua-kich-tran",
                "ban-trang-diem-bac-au",
            ],
        },
    ]

    col_objs = {}
    for c in collections_data:
        obj = (
            db.query(ProductCollection)
            .filter(ProductCollection.slug == c["slug"])
            .first()
        )
        if not obj:
            obj = ProductCollection(
                name=c["name"],
                slug=c["slug"],
                description=c["desc"],
                image_url=c["image_url"],
                is_featured=c["is_featured"],
            )
            db.add(obj)
            db.commit()
            db.refresh(obj)
            print(f"Added collection: {obj.name}")
        col_objs[c["slug"]] = (obj, c["products"])

    # Assign collections to products
    for col_slug, (col_obj, prod_slugs) in col_objs.items():
        for p_slug in prod_slugs:
            prod = db.query(Product).filter(Product.slug == p_slug).first()
            if prod and col_obj not in prod.collections:
                prod.collections.append(col_obj)
    db.commit()

    print(f"Seed completed. Added {count} new products.")
    db.close()


if __name__ == "__main__":
    seed()
