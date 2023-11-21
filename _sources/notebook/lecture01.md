---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.15.2
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

+++ {"id": "f743060006afda4b"}

# สำรวจชุดข้อมูลทิป

**จุดประสงค์การเรียนรู้**
1. การรู้จักและใช้งาน `DataFrame` และ `Series` เบื้องต้น กับชุดข้อมูลจริง
2. ตอบคำถามเกี่ยวกับสถิติการได้รับทิปจากข้อมูลที่มี
3. จัดการข้อมูลในเบื้องต้น
4. วาดกราฟเบื้องต้น ได้แก่ กราฟแท่ง, scatter plot, และ histogram ด้วย `plotly`

*ก่อนเริ่ม* นักศึกษาสามารถ google หาข้อมูลได้หรือไม่ว่า
- เว็บไซต์ทางการ (official) ของ `Pandas` คือเว็บไหน
- `Pandas` เวอร์ชันแรกถูกเผยแพร่ในปี ค.ศ. เท่าไร
- ที่มาของชื่อ `Pandas` มาจากอะไร

+++ {"id": "uY3_c6hc-gGp"}

**เริ่มต้นบทเรียน**

+++ {"id": "1OWJ9WDv-VaM"}

พนักงานเสิร์ฟคนหนึ่งบันทึกข้อมูลเกี่ยวกับทิป ที่เขาได้รับขณะทำงานที่ร้านอาหารแห่งหนึ่งในสหรัฐอเมริกา  ซึ่งเมื่อเขาได้ทิปแต่ละครั้ง เขาจะบันทึกข้อมูลลงในไฟล์ `tips.csv` อย่างสม่ำเสมอ ตลอดช่วงเวลาหลายเดือนที่ผ่านมา โดยรายละเอียดของค่าที่เขาบันทึกแต่ละครั้ง มีดังนี้

| ค่าที่  | รายละเอียด |
|:---:|:---|
|1| บิลค่าอาหาร (ดอลลาร์) |
|2| ทิปที่เขาได้รับ (ดอลลาร์) |
|3| เพศของผู้จ่ายบิลค่าอาหาร |
|4| มีคนสูบบุหรี่หรือไม่ (ในโต๊ะของลูกค้าในบิลนั้น)  |
|5| วันที่ได้รับทิป  |
|6| เวลาที่จ่ายบิล |
|7| จำนวนลูกค้าในบิลนั้น |

พนักงานเสิร์ฟคนนี้ ได้แชร์ไฟล์ `tips.csv` มาให้นักศึกษา โดยร้องขอให้นักศึกษาศึกษาข้อมูลที่มีในเบื้องต้น เพื่อตอบคำถามที่เขาอยากรู้ ซึ่งในขั้นแรก นักศึกษาจึงได้ดาวน์โหลดและอ่านข้อมูลไฟล์ `tips.csv` เข้ามาโดยใช้คำสั่ง `read_csv()` [(คู่มือ)](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html) ของ `Pandas`ดังนี้

+++ {"id": "99zE1DhI4YJy"}

## **การอ่านข้อมูล**

```{code-cell} ipython2
:id: 37b18074a1c02e4f

import pandas as pd
tips = pd.read_csv('https://raw.githubusercontent.com/kasemsit/269382/main/dataset/tips.csv')
```

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: 41ea04f37ab5c719
outputId: 28e949dd-455d-4d0d-cf76-1ba6556afec8
---
print(tips)
```

+++ {"id": "0n_nEJcWqgyG"}

ทั้งนี้ ไม่จำเป็นต้องใช้ฟังก์ชัน `print()` ในการพิมพ์ตารางก็ได้ โดย Google Colab สามารถแสดงผลตาราง `tips` ได้สวยงาม เพียงเรียกตัวแปร `tips` ในบรรทัดสุดท้ายของเซลล์

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 423
id: CS2Vq8x_rJ4Y
outputId: e63d10a2-7e7a-4416-b4a8-7a389f4f2a5a
---
# แสดงตาราง
tips
```

+++ {"id": "2bc8674bb25cbc05"}

จากข้อมูล เนื่องจากนักศึกษาไม่ได้เป็นคนเก็บข้อมูลเอง ดังนั้นเพื่อความแน่ใจ นักศึกษาจึงตรวจสอบข้อมูลที่ได้มาในเบื้องต้น ตามลำดับ ด้วยการตั้งคำถามเหล่านี้

## คำถามขั้นแรกเกี่ยวกับตัวแปรตารางที่อ่านเข้ามา

+++ {"id": "c1dhJ2ngkdmd"}

### ตัวแปร `tips` เป็นตัวแปรชนิดใดในภาษา Python

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: 2f44d40aab40f347
outputId: ea58c01d-7549-41d9-b0d9-363c6acc6c2f
---
x = type(tips)
print(f'ชนิดข้อมูลคือ {x}')
```

+++ {"id": "8sGnwpiQl8Xk"}

จะเห็นว่า ตัวแปร `tips` เป็นตัวแปรชนิด `DataFrame` ที่ถูกนิยามไว้ใน `Pandas`

**ทบทวน: ชนิดตัวแปรพื้นฐานในภาษา `Python`**

1) ชนิดตัวแปรที่เก็บได้ค่าเดียว

|ชนิดตัวแปร  | ความหมาย |ตัวอย่าง |
|:-- |:-- |:--
|`int` | ตัวแปรเก็บค่าจำนวนเต็ม (Interger) | `100` |
|`float` | ตัวแปรเก็บค่าจำนวนทศนิยม (Float) | `1.0` |
|`bool` | ตัวแปรเก็บค่าตรรกะ (Boolean) | `True`,`False`  |

2) ชนิดตัวแปรที่เก็บได้หลายค่า (container)

|ชนิดตัวแปร  | ความหมาย | ตัวอย่างที่มีสมาชิก 0 ตัว | ตัวอย่างที่มีสมาชิก 1 ตัว | ตัวอย่างที่มีสมาชิกหลายตัว |
|:-- |:-- |:--|:-- |:-- |
|`str` | String | '' หรือ "" | 'A' | `'123'`,`'hello'` |
|`list` | List | `[]` หรือ `list()` | `[2]` | `[3,2,'hello',`False`, 1.0]` |
|`tuple` | Tuple | `()` หรือ `tuple()` | `(2,)` | `(3,2,'hello',`False`, 1.0)`|
|`set` | Set | `set()` | `{2}` | `{3,2,'hello',`False`, 1.0}` |
| `dict` | Dictionary | `{}` หรือ `dict()` | `{2:3}` | `{1:3,2:2,'T':'hello'}` |

+++ {"id": "AUCj2muk39mc"}

**คำถาม:** ลำดับเลข 0,1,2,...,244 ที่แสดงจากตัวแปร `tips` เป็นค่าที่เก็บในไฟล์ `csv` ใช่หรือไม่

+++ {"id": "e56e70e53e75684c"}

### ข้อมูลมีกี่แถวและกี่คอลัมน์

**วิธีที่ 1** ใช้คำสั่ง `len()` นับจำนวนแถว

```{code-cell} ipython2
x = len(tips)
print(f'จำนวนแถวคือ {x}')
```

+++ {"id": "uk3D6NARfxyP"}

**วิธีที่ 2** ใช้คำสั่ง `DataFrame.shape` นับจำนวนแถวและจำนวนคอลัมน์

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: ed59789bf35d2bb0
outputId: 400caedc-6690-4167-ee46-ad0884be8479
---
x = tips.shape
print(f'(แถว,คอลัมน์) มีจำนวนคือ {x}')
```

+++ {"id": "78780a90bd944c1"}

`tips.shape` จะให้ `tuple` ที่เก็บจำนวนแถวและจำนวนคอลัมน์ตามลำดับ

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: cc737d95dd092701
is_executing: true
outputId: 1a988762-5825-40a3-efde-03c7fafa24b3
---
n_row = tips.shape[0]
n_col = tips.shape[1]
print(f'ข้อมูลมี {n_row} แถว and {n_col} คอลัมน์')
```

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: b8de84fd9b1d7630
outputId: 11ea0146-fd7b-4b4f-d67a-22740b1bc7ea
---
n_row, n_col = tips.shape
print(f'ข้อมูลมี {n_row} แถว and {n_col} คอลัมน์')
```

+++ {"id": "mTvG8hBSgI9-"}

### ตัวอย่างข้อมูลบางแถวในตารางมีค่าอะไรบ้าง

+++ {"id": "gyXbPwzLlIzM"}

**แบบที่ 1** `DataFrame.head()` เช่น ดูเฉพาะ 2 แถวแรก

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: e37173d3abfb9d83
outputId: 805c0113-f616-4685-e553-a741f4049f85
---
tips.head(2)
```

+++ {"id": "Njs6OLdSijhv"}

จะเห็นว่า แถวแรกคือแถวที่ 0, แถวถัดมาคือแถวที่ 1

+++ {"id": "7lhq4Y_oiQjQ"}

**แบบที่ 2** `DataFrame.tail()` เช่น ดูเฉพาะ 3 แถวสุดท้าย

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: RFBAWR12g2aT
outputId: 555413dd-1b08-4bbb-a6de-5f178439e941
---
tips.tail(3)
```

+++ {"id": "JuNVwVLRifaX"}

จะเห็นว่า แถวสุดท้ายคือแถวที่ 243 เพราะข้อมูลเป็นตารางที่มีทั้งหมด 244 แถว นั่นเอง

+++ {"id": "vG25KpJMinZA"}

**แบบที่ 3** `DataFrame.sample()` เช่น สุ่มมา 4 แถว

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: jhOzbffnhkGR
outputId: d3dcc9ad-7060-46b9-e830-1a0e5d047848
---
tips.sample(4)
```

+++ {"id": "bU54LF_4it2n"}

จะเห็นว่า ถ้าเรียกคำสั่งนี้ซ้ำ ๆ จะได้ข้อมูลที่ไม่ซ้ำแถวกัน อย่างไรก็ตาม หากต้องการให้สุ่มได้ซ้ำแบบเดิม (อาจทำเพื่อแสดงให้คนอื่นดู) ก็อาจส่งค่า `random_state` ให้ฟังก์ชัน `sample` ด้วย

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: kFohNJtBh25x
outputId: c5d38ae5-7d28-4042-b157-338cb9109e1d
---
tips.sample(4, random_state=123)  # กำหนดค่า random_state เป็นจำนวนเต็มได้ตามต้องการ
```

+++ {"id": "M1ilyk63jwD2"}

หมายเหตุ: ฟังก์ชันของ `Pandas` (รวมถึงฟังก์ชันอื่น ๆ ที่นักศึกษาจะได้พบในอนาคต) ที่มีพฤติกรรมในลักษณะของการสุ่มค่า มักจะสามารถกำหนดค่า `random_state` เพื่อล็อกผลของการสุ่มได้ เช่น `sklearn.model_selection.train_test_split(..., random_state=8888)`  เป็นต้น

+++ {"id": "nSdhyfYvnluI"}

### ต้องการรายงานเกี่ยวกับคอลัมน์ในตาราง

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: uMl2s3eUnxu3
outputId: ca21609e-f9e9-4135-aeb5-274cc655e85e
---
tips.info()
```

+++ {"id": "hil_JnsQn_WU"}

สิ่งที่คำสั่ง `DataFrame.info()` รายงานออกมา คือ
1. ชื่อคอลัมน์
2. จำนวนข้อมูลในแต่ละคอลัมน์ ไม่รวม missing value เช่นจะเห็นว่า คอลัมน์ชื่อ `total_bill` มีข้อมูลอยู่ 245 ค่า (non-null) และไม่มีข้อมูลที่สูญหาย (null) เลย
3. Dtype คือชนิดของตัวแปรที่เก็บในคอลัมน์หนึ่ง ๆ เช่น คอลัมน์ `tip` เก็บข้อมูลชนิด `float` ขนาด 64 บิต หรือคอลัมน์ `size` เก็บข้อมูล `int` ขนาด 64 บิต เป็นต้น สำหรับใน `Pandas` มีการนิยามตัวแปรเพิ่มขึ้นอีกหลายชนิด โดยที่สำคัญที่คำสั่ง `DataFrame.info()` ก็คือ ตัวแปรชนิด `object` ซึ่งสามารถเก็บข้อมูลได้แบบผสม (mixed-type)

+++ {"id": "uD6qIbveqXGz"}

### จะเข้าถึงเฉพาะบางคอลัมน์ที่ต้องการได้อย่างไร

+++ {"id": "k-SVMiHmrZBF"}

**แบบที่ 1** เข้าถึงคอลัมน์เดียวด้วยชื่อคอลัมน์

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: oGIerVd0rTTc
outputId: 44d2e9fa-f194-4276-8db9-c8e08ff73ebf
---
s = tips['smoker']
s
```

+++ {"id": "FFmUK3AI8hAs"}

หรือ ใช้เครื่องหมายจุด ตามด้วยชื่อคอลัมน์ก็ได้

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: aazImMtD8mvv
outputId: 126ed07d-6ca2-4b0e-bddb-831a0ea454e3
---
s = tips.smoker
s
```

+++ {"id": "j5xV6q7FrnAn"}

**แบบที่ 2** เข้าถึงหลายคอลัมน์ด้วยรายการของชื่อคอลัมน์

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 423
id: fZhRpSBlrmLo
outputId: c6051c1a-0b78-4f84-d505-73ad7afff3a1
---
df = tips[['smoker','time','sex']]
df
```

+++ {"id": "h_LmrR2Gs0cv"}

**คำถาม** ค่า `tips['smoker']` และ `tips[['smoker']]` เป็นตัวแปรประเภทเดียวกันหรือไม่ นักศึกษาตรวจสอบได้อย่างไร?

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: 0_0z7wDktP4l
outputId: 11bf2500-187d-4858-d922-9c1699ae07b0
---
print(type(tips['tip']))
print(type(tips[['tip']]))
print(type(tips[['tip','time','sex']]))
```

+++ {"id": "Q99HyrawtnqW"}

**ข้อสังเกตุทางเทคนิค** `DataFrame` vs. `Series`

ตัวแปรประเภท `DataFrame` ไม่เหมือนกับตัวแปรชนิด `Series` กล่าวคือ `Series` คือตัวแปรที่เก็บข้อมูล 1 มิติ แต่ `DataFrame` เก็บข้อมูล 2 มิติ ดังแสดงได้จากคำสั่งต่อไปนี้

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: JPheg4oJy2YP
outputId: ba0e45b6-fb67-4ec6-817f-0a3e190e27a7
---
s = tips['sex']
df = tips[['sex']]
print(f'shape of s = {s.shape}')
print(f'shape of df = {df.shape}')
print(f'len of s = {len(s)}')
print(f'len of df = {len(df)}')
```

+++ {"id": "Gc-mA96vzIAH"}

จะเห็นว่า shape ของ `Series` เป็น `tuple` 1 มิติ แต่ของ `DataFrame` เป็น 2 มิติ ดังนั้น ในทางปฏิบัติ ควรจะทราบว่าตัวแปรที่กำลังใช้งานเป็น `Series` หรือ `DataFrame` เพื่อที่จะเข้าใจการทำงานได้ถูกต้อง

ถ้าหากต้องการแปลง `Series` ที่มีอยู่แล้ว ให้เป็น `DataFrame` (ที่มี 1 คอลัมน์) ก็สามารถทำได้โดยใช้คำสั่ง `Series.to_frame()`

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: hKLLmTCU1o4o
outputId: a14f052e-ae57-491c-d781-1158742f572d
---
s.to_frame()
```

+++ {"id": "QQ4JmS3emkhm"}

### ต้องการ List ของชื่อคอลัมน์และชื่อ index

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: H_Z3gLy6nBkq
outputId: 87386194-f931-430b-8655-05dd1ded921e
---
tips.columns
```

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: 4j5KPb1hnJLq
outputId: ecb2a92c-13b5-4089-9a99-af5f30235a08
---
print(tips.columns.tolist())  # ให้ชนิดข้อมูลเป็น List ของ Python
print(list(tips.columns))
```

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: FjsUnuGdnFiK
outputId: 4ed405d3-a423-4990-ad1c-adb238d43895
---
tips.index  # จะเห็นว่า index ของแถวเป็นเลข autorun
```

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: eXvldHvKnMWC
outputId: d63518ba-a0d7-46fa-8004-b86e31317908
---
print(tips.index.tolist())  # ให้ชนิดข้อมูลเป็น List ของ Python
print(list(tips))
```

+++ {"id": "8Dl4aVxX0vJW"}

**ข้อสังเกตุ** `tips.columns` และ `tips.index` ไม่ใช่ตัวแปร List ดั้งเดิมในภาษา `Python` แต่เป็นชนิดตัวแปรที่นิยามไว้ใน `Pandas` เอง ดังนั้น หากต้องการแปลงเป็น List อาจใช้คำสั่ง `.tolist()` หรือไม่ก็ `list()` ก็ได้

คำสั่ง `.tolist()` ยังใช้ได้กับค่าอื่น ๆ ได้ เช่น แปลง `Series` ให้เป็น List ของ Python เป็นต้น

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: YrtO5IUr12Z4
outputId: cde6ac5a-c23b-4c4c-a6ec-798616d3d1ee
---
s = tips['sex']
print(s.tolist())
```

+++ {"id": "mHdTGPndPIyJ"}

## เกี่ยวกับสถิติอย่างง่ายและการนับจำนวน

+++ {"id": "l53pquVm9qE8"}

### ต้องการทราบค่าสถิติเบื้องต้น

คำถามที่ต้องการทราบในเบื้องต้น

+ พนักงานเสิร์ฟได้ทิปเฉลี่ยกี่ดอลลาร์?
+ เขาได้ทิปสูงสุดกี่ดอลลาร์?
+ กลุ่มลูกค้าที่เขาเคยเสิร์ฟมากันมากที่สุดกี่คน
+ จากชุดข้อมูลนี้ เขาทำเงินจากทิปมาแล้วกี่ดอลลาร์

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 300
id: adikYl93_XEG
outputId: 91eb3493-a761-4b98-bd4d-085437ef561f
---
tips.describe()
```

+++ {"id": "JDTeI_Pr_apd"}

ฟังก์ชัน `DataFrame.describe()` ข้างต้น แสดงผลเป็น `DataFrame` ที่สรุปค่าทางสถิติเบื้องต้น อย่างไรก็ตาม แม้ว่าข้อมูลทิปมีทั้งหมด 7 คอลัมน์ แต่ค่าสถิติที่รายงาน มีเฉพาะคอลัมน์ที่เก็บชนิดข้อมูลตัวเลข

โดยทั่วไป มักจำเป็นต้องการนำค่าทางสถิติไปใช้คำนวณต่อ, ต้องการคำนวณค่าสถิติเพียงบางค่า, หรือต้องการคำนวณค่าสถิติอื่น ๆ เช่น `sum` ที่ `DataFrame.describe()` ไม่ได้มีให้

วิธีการคำนวณทำ ดังนี้

+++ {"id": "KkT_o0ztd-oA"}

#### คำนวณค่าสถิติของ `Series`

กรณีที่เข้าถึงเพียงคอลัมน์เดียว แต่ละคอลัมน์ก็คือตัวแปรประเภท `Series` สามารถคำนวณค่าสถิติได้ ดังนี้

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: jsm94LyZbEY8
outputId: 4f7cd547-64f6-4667-f923-73782c06808a
---
tips['tip'].mean()  # ค่าเฉลี่ย (ได้เป็น float)
```

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: 64_y1Ok3bHjA
outputId: d3a7663b-e523-42cd-a864-58401e64529c
---
tips['tip'].std()  # ค่า SD โดย Default จะใช้สูตร SD ที่มี degree of freedom = 1 หรือก็คือค่า SD ของกลุ่มตัวอย่าง (ไม่ใช่ SD ของประชากร)
```

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: _Kl_BdzFamEu
outputId: f48acb6c-260a-4c45-e72e-77717588c838
---
tips['tip'].sum()  # ผลรวม
```

+++ {"id": "trROVEdJei8S"}

สำหรับค่าสถิติอื่น ๆ เช่น

- `tips['tip'].max()`
- `tips['tip'].min()`
- `tips['tip'].median()`
- `tips['tip'].count()`

เนื่องจากค่าสถิติมีหลากหลาย จึงสามารถสั่งให้คำนวณในคราวเดียวได้ ด้วยคำสั่ง `DataFrame.agg()`

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: PMOueBU_ehlF
outputId: f5f052e4-c839-43d2-9cba-80fc0e09df11
---
tips['tip'].agg(['sum','min','max','mean','std','median'])
```

+++ {"id": "IFYXhaUDgGyA"}

#### การคำนวณค่าสถิติของ `DataFrame`

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: YGDPfZQZgMrx
outputId: ab94718d-aaae-4d41-9f3d-fcf478c3db32
---
tips[['tip','total_bill']].mean()  # ค่าเฉลี่ยได้เป็น Series
```

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 143
id: EY0vDhdlgzyk
outputId: 42ed34f7-18d8-4648-cc1d-2169dc8e7024
---
tips[['tip','total_bill']].agg(['mean','std','max'])  # ค่าเฉลี่ยได้เป็น DataFrame
```

+++ {"id": "3FVdDeyNAOIX"}

### อยากรู้เกี่ยวกับค่าที่เป็นไปได้ในแต่ละคอลัมน์

- คอลัมน์ `time` เก็บค่าอะไรไว้บ้าง และกี่ค่า?


โดยตัวอย่างต่อไปนี้ แสดงการใช้ฟังก์ชันของ `Series`

+++ {"id": "U0618H0iB2TU"}

**แบบที่ 1** ต้องการทราบแต่ค่า

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: kqUJ8a2iCCIJ
outputId: 313b90a5-77c9-476c-bd31-f8a364e16e8e
---
x = tips['time'].unique()
print(x)
```

+++ {"id": "-WuFIqg2COmx"}

**แบบที่ 2** ต้องการทราบแต่จำนวนแบบ

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: FzlBZTneBsLB
outputId: 545791b1-3fdc-4423-f8ff-b19a9c291562
---
x = tips['time'].nunique()
print(x)
```

+++ {"id": "0cSzZYxYCW2R"}

**แบบที่ 3** ต้องการทราบจำนวนในแต่ละแบบ

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: AlQYRadLAisw
outputId: 2fe50524-a707-4c49-a171-956e119fefd2
---
x = tips['time'].value_counts()  # ได้ผลลัพธ์เป็น Series
print(x)
```

+++ {"id": "arViK2jwBR64"}

จากการลองนับค่าในคอลัมน์ `time` พบว่ามีค่าที่เป็นไปได้ 2 แบบคือ `Dinner` และ `Lunch` ซึ่งสมเหตุสมผล เพราะนักศึกษาทราบจากพนักงานเสิร์ฟว่า เขาทำงานสองช่วงเวลา คือ ตอนเที่ยงและตอนเย็น

+++ {"id": "laIzrnLUCxjC"}

นอกจากนี้ คำสั่ง `value_counts()` ยังสามารถใช้ได้กับ `DataFrame` เช่นกัน ยกตัวอย่างเช่น

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: JWVKG6X7Axxl
outputId: 19a23c70-cf39-4bee-e0d3-72acb6d660c4
---
x = tips[['sex','time']].value_counts()  # ได้ผลลัพธ์เป็น Series เช่นกัน แต่เป็น Series ที่มี Index หลายชั้น (Multi-Index)
print(x)
print(f'ข้อมูลที่รายงานจาก value_counts() เป็นชนิด {type(x)}')
```

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: OPFLrUluFpv9
outputId: 1672fa33-7c43-4184-83d0-38c25fa10fcc
---
x.index
```

+++ {"id": "09oGKPVkF3jk"}

### การสร้างตารางแบบสองทาง (Two-way table)

สมมติว่าต้องการตอบคำถามต่อไปนี้

- ผู้ชายจ่ายทิปมื้อเที่ยงหรือมื้อดินเนอร์มากกว่ากัน? มีวันไหนจ่ายมากเป็นพิเศษไหม? แล้วถ้าเทียบกับผู้หญิงล่ะ?

ก็อาจสร้างตารางแบบสองทาง เพื่อนับจำแนกความถี่ของค่าแต่ละคู่ที่สนใจด้วยคำสั่ง `pd.crosstab`

+++ {"id": "L20n1IMOLXVe"}

**ตัวอย่างที่ 1** ไขว้ระหว่างค่าในคอลัมน์ `sex` และ `time`

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 143
id: iLTPxJmlKnbz
outputId: 5d3c7d37-5b2a-4c78-c6e2-1f31481824bd
---
sex = tips['sex']
time = tips['time']
x = pd.crosstab(index=sex, columns=[time])
x
```

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: EXmyEKwiLxM1
outputId: e70e7411-cb01-4751-9a33-d5c03fcece5d
---
print(x.columns)
print(x.index)
```

+++ {"id": "E6cP_hHkQUnB"}

**ข้อสังเกตุ** index ของแถว ไม่จำเป็นต้องเป็นตัวเลขก็ได้ ดังเช่นในกรณีของตารางไขว้ข้างต้น ที่เป็น `DataFrame` ที่มี index คือ 'Female' กับ 'Male'

+++ {"id": "82jq2H00Ljj2"}

**ตัวอย่างที่ 2** ไขว้ระหว่างค่าในคอลัมน์ `sex` และ `(day, time)`

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 174
id: tl1fDxY-AYo-
outputId: 7f3ffcc4-c9dc-4ecf-9fa4-f6848e30844b
---
sex = tips['sex']
day = tips['day']
time = tips['time']
x = pd.crosstab(index=sex, columns=[day, time])
x
```

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: b4rG6nYML42k
outputId: 72d5903f-9231-455b-b302-e03db00ed9e1
---
print(x.columns)
print(x.index)
```

+++ {"id": "StNipD6cRPT9"}

## เกี่ยวกับการเลือกแถวด้วยของ `DataFrame` ด้วยตรรกะ `True/False`

ใน `Pandas` เมื่อนำข้อมูล 1 คอลัมน์ซึ่งเป็นชนิด `Series` มาเปรียบเทียบกับค่า ๆ หนึ่ง จะได้ผลลัพธ์เป็นค่าตรรกะ `True` หรือ `False` ดังตัวอย่างเช่น

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: zZttB0j9qOxI
outputId: 6a66e197-1d5d-4751-ff54-1b879ad985bf
---
tips['tip'] <= 1.1
```

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: KPBF1Sl1qLAG
outputId: e4f2d330-53af-41a0-8c16-9059691b1f6d
---
tips['day'] == 'Sun'
```

+++ {"id": "Bj671-JlsILQ"}

การเปรียบเทียบ `Series` กับค่า ๆ หนึ่ง (หรือจะกับอีกคอลัมน์หนึ่ง) จะได้ผลลัพธ์เป็น `Series` ที่เก็บข้อมูลชนิด `bool` (`True` หรือ `False`) โดย `Series` ดังกล่าวมีประโยชน์คือ สามารถนำไปใช้เลือกเฉพาะบางแถวในตารางได้ โดยจะกรองได้แถวที่มีค่าใน `Series` เป็น `True`

สมมติว่ามีข้อมูลใน `DataFrame` ชื่อ `df` และ `Series` ชื่อ `flags` ที่เป็นชนิด `bool` จะสามารถการกรองค่าแถวของ `df` ด้วยตรรกะ `flags` ได้ 2 แบบ คือ

1. `df.loc[flags]`
2. `df[flags]`   (เป็นรูปแบบย่อของแบบที่ 1 ซึ่งอาจสับสนกับการเข้าถึงคอลัมน์ในหัวข้อ Q1.5 ได้ แต่ก็เป็นที่นิยมใช้)

+++ {"id": "7msmIHlCoKXy"}

### ต้องการเฉพาะแถวที่มีค่า `day` เท่ากับ `Sun`

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 423
id: twBZFA3-t8lZ
outputId: 6b432698-0f74-408b-e292-392f7df5d27b
---
flags = (tips['day'] == 'Sun' )  # ตัวชื่อตัวแปรว่า flags เพราะว่าถ้า True ก็หมายถึงยกธงเลือก, False ก็หมายถึงไม่เลือก
tips.loc[flags]  # แบบเต็มใช้ .loc[]
```

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 423
id: kN4HkIeOJcA0
outputId: 0d9616c1-6f83-432b-86e2-155052cda296
---
tips[flags]   # แบบย่อ โดยละ .loc
```

+++ {"id": "3D5-ywwlJhCr"}

**ลองทำ:** ตรวจสอบความเข้าใจ ด้วยการลองคำสั่งต่อไปนี้

| คำสั่ง | ผลลัพธ์ |
|:--|:--|
|`tips['day']` | ให้คอลัมน์ชื่อ `day` |  
|`tips[0]` | Error เพราะไม่มีคอลัมน์ชื่อ `0`  |
|`tips['Sun']` | Error เพราะไม่มีคอลัมน์ชื่อ `Sun` |
|`tips[tips['day']=='Sun']]` | ให้แถวที่มี `day` เท่ากับ `Sun` |
|`tips.loc[tips['day']=='Sun']]` |  ให้แถวที่มี `day` เท่ากับ `Sun` |   

การเข้าถึงค่าใน `DataFrame` ใน `Pandas` มีรายละเอียดมากพอสมควร ดังนี้ ณ จุดนี้ จะขอเพียงเท่านี้ก่อน

+++ {"id": "bDxMUJR1nZbB"}

### ต้องการเฉพาะแถวที่มีค่า `tip` น้อยกว่าหรือเท่ากับ `1.1`

+++ {"id": "Ih1L20uwu3nw"}

**วิธีที่ 1** เปรียบเทียบด้วยเครื่องหมาย `<=`

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 237
id: l8HvIwOkofh9
outputId: 8061b895-7629-4c53-cc1a-4366cafaee6f
---
flags = (tips['tip'] <= 1.1)
tips[flags]
```

+++ {"id": "cZbwSVUhu9Tn"}

**วิธีที่ 2** เปรียบเทียบด้วยเครื่องหมาย `>` แล้วใช้นิเสธ `~`

การกลับตรรกของ `Series` ชนิด `bool` ให้เป็นทางตรงกันข้าม ทำได้โดยใช้สัญลักษณ์ `~` (ไม่ใช่ `not`)

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 237
id: VHov02w3vHhT
outputId: 5f834fb8-5be3-4d07-e7f0-6ddc719559a3
---
flags = (tips['tip'] > 1.1)
tips[~flags]         # ผลลัพธ์เทียบเท่ากับการเทียบ <= 1.1
```

+++ {"id": "5jgivy00uilT"}

### ต้องการเฉพาะแถวที่มี `tip` ในช่วง 1.25 ถึง 1.35 ด้วยตรรกะ `&`

+++ {"id": "z9WqXYfVyd_u"}

การกระทำระหว่าง `Series` ชนิด `bool` 2 `Series` จะใช้สัญลักษณ์ `&` (ไม่ใช่ `and`)

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 174
id: b23pfEtCx3Vn
outputId: 714bb2cc-1691-4d9e-b88d-3d2fbc3eceab
---
flags_1 = (tips['tip'] >= 1.25)
flags_2 = (tips['tip'] <= 1.35)
tips[flags_1 & flags_2]
```

+++ {"id": "DSGWUXj0zTNy"}

### ต้องการเฉพาะแถวที่มี `tip` ที่น้อยกว่าเท่ากับ 1.1 หรือมากกว่าเท่ากับ 9.0 ด้วยตรรกะ `|`

การกระทำระหว่าง `Series` ชนิด `bool` 2 `Series` จะใช้สัญลักษณ์ `|` (ไม่ใช่ `or`)

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 300
id: Ff9KtWQ4uiBT
outputId: 6c0f2b6d-5d74-4839-c0b3-3d960a155ad0
---
flags_1 = (tips['tip'] <= 1.1)
flags_2 = (tips['tip'] >= 9.0)
tips[flags_1 | flags_2]
```

+++ {"id": "PJT9TI6v1gUl"}

ทั้งนี้ ตรรกกะ  `(tip <= 1.1) & (tip >= 9.0)` เทียบเท่ากับ `~((tip > 1.1) | (tip < 9.0))`

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 300
id: ZQNjD3U50sHx
outputId: fa7125ce-aefa-4c4a-fff2-ac16c011cc55
---
flags_1 = (tips['tip'] > 1.1)
flags_2 = (tips['tip'] < 9.0)
tips[~(flags_1 & flags_2)]
```

+++ {"id": "jYwCdvNUvp8e"}

โดยสรุป โอเปอร์เรเตอร์ในการเปรียบเทียบ ที่เป็นไปได้มีดังนี้

| เปรียบเทียบ | ความหมาย |
|:--:|:-- |
| `==` | เท่ากันหรือไม่ |
| `!=` | ไม่เท่ากันหรือไม่ |
| `>` หรือ `>=` | มากกว่า, มากกว่าเท่ากับ |
| `<` หรือ `<=` | น้อยกว่า, น้อยกว่าเท่ากับ |

| ตรรกะ | ความหมาย |
|:--:|:-- |
| `~` | นิเสธ |
| `&` | และ |
| `\|` | หรือ |

+++ {"id": "UjjgC7QnEg07"}

### **เลือกแถวด้วยตรรกะ แต่อยากได้เพียงบางคอลัมน์**

จาก Q3.1 ถึง Q3.4 นักศึกษาสามารถเลือกแถวตามเงื่อนไขที่ต้องการได้แล้ว แต่ไม่อยากได้ทุกคอลัมน์ ก็สามารถทำได้ 2 แบบ ดังตาราง

| แบบที่  | คำสั่ง | ยกตัวอย่าง | คำแนะนำ |
|:--:|:--:|:-- |:-- |
|1 | `df.loc[flags, ชื่อคอลัมน์หรือ list ชื่อคอลัมน์]`|  `tips.loc[flags, 'sex']`  | ควรใช้ |
|2 | `df.loc[flags][ชื่อคอลัมน์หรือ list ชื่อคอลัมน์]`|  `tips.loc[flags]['sex']` | ไม่ควรใช้ |

โดยที่ `df` คือ `DataFrame` และมีและ `flags` เป็น `Series` ชนิด `bool`

**ระวัง:** ผู้หัดใช้ `Pandas` มือใหม่ มักใช้แบบที่ 2 ซึ่งเป็นแบบควรหลีกเลี่ยง แม้ว่าจะได้แถวที่ต้องการเหมือนกัน ซึ่งความแตกต่างระหว่างสองแบบนี้ จะเกิดขึ้นในกรณีที่ต้องการเขียนค่าลงใน `DataFrame` (ซึ่งเกินเนื้อหาของคาบนี้) ดังนั้นจึงขอให้นึกศึกษาทำความคุ้นเคยกับแบบที่ 1 ไว้ก่อน แต่หากอยากใช้แบบที่ 2 ก็ย่อมได้ แต่ขอให้ทราบถึงข้อจำกัดของมัน

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: l07uHORLR36N
outputId: afd6f3eb-4b14-438a-f872-0e78d08f075a
---
flags = (tips['tip'] > 1.1)
tips.loc[flags]['sex']  # ไม่ควรใช้แบบนี้
```

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: p6HcbFXYSXc0
outputId: b0d424a6-45e2-46e0-c352-e090a227e2ba
---
flags = (tips['tip'] > 1.1)
tips.loc[flags, 'sex']  # ควรใช้แบบนี้
```

+++ {"id": "upLBDRYhVlNR"}

หรือกรณีที่ต้องการมากกว่า 1 คอลัมน์

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 423
id: FtDkBg9JFMkf
outputId: f66babb1-1fc3-4cb4-8d06-d3d06138045c
---
flags = (tips['tip'] > 1.1)
tips.loc[flags, ['total_bill','sex']]  # ต้องการ 2 คอลัมน์
```

+++ {"id": "Bq2-F6AYUVTS"}

ทั้งนี้ คำสั่ง
```python
df.loc[flags, ชื่อคอลัมน์หรือ list ชื่อคอลัมน์]
```
ไม่สามารถละ `.loc` ได้ ไม่เหมือนกับที่ `df[flags]` เป็นรูปย่อของ `df.iloc[flags]` ดังนั้น

```python
tips[flags, 'sex']      # คำสั่งนี้ Error (ขอให้นักศึกษาลองทำดู)
```
จะไม่สามารถทำงานได้

+++ {"id": "x5NCjChs33Fu"}

### **มีแถวที่ซ้ำกันบ้างไหมนะ**

สามารถดูแถวที่ซ้ำด้วย `DataFrame.duplicated()` โดยจะให้ผลลัพธ์เป็น `Series` ชนิด `bool` โดยแถวที่ซ้ำทั้งแถวกับแถวอื่น ก็จะมีค่าเป็น `True` หากแถวนั้นไม่ซ้ำกับแถวไหนเลย ก็จะมีค่าเป็น `False` (เป็นกรณีที่กำหนดพารามิเตอร์ `keep=False` หากกำหนดให้ `keep` เป็นค่าอื่น ก็จะแตกต่างออกไป)

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 143
id: wpLR-gaBROXC
outputId: 60a3f31c-6ed0-4440-e454-6fea16587ce1
---
flags = tips.duplicated(keep=False)
tips[flags]
```

+++ {"id": "YWspGaqkBzWO"}

*จงตอบคำถาม:*
1. พารามิเตอร์ `keep` มีค่าที่เป็นไปได้ 3 แบบ คือ `False`, `'first'`, และ `'last'` แล้วแต่ละแบบแตกต่างกันอย่างไร
2. หากไม่ระบุ `keep` แล้ว `Pandas` จะได้ผลอย่างไร

+++ {"id": "hqQ6FT3oFoq1"}

`DataFrame.duplicated()` จะพิจารณาว่าทั้งแถวซ้ำกันหรือไม่ แต่ในกรณีที่ต้องการให้พิจารณาเฉพาะเพียงบางคอลัมน์ในแถว ก็สามารถระบุได้ด้วยพารามิเตอร์ `subset`

เช่น (อาจด้วยเหตุผลบางประการ) สมมติว่าสนใจคู่ `day` และ `time` แล้วต้องการดึงเฉพาะแถวที่ปรากฎคู่นี้ครั้งแรก
 ก็สามารถทำได้ ดังนี้

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 237
id: d886Z2jnDERR
outputId: 1c2064fb-175f-4abb-bfd9-678fbe41df44
---
flags = tips.duplicated(subset=['day','time'])  # แถวที่มีคู่ day และ time ซ้ำกันจะถูก flag ว่า True เว้นแต่เป็นคู่แรกที่เจอ
flags = ~flags # กลับตรรกะเพื่อเลือกเฉพาะแถวแรกที่ซ้ำ
tips[flags]
```

+++ {"id": "F6irZRfkRlUX"}

จากตารางข้างต้น ตีความได้ว่า คู่ `(Thur,	Lunch)` ถูกพบครั้งแรกที่แถว `index=77` เป็นต้น

+++ {"id": "Rgu4Sc7gT8FR"}

### ตรรกะ OR และ AND ของทั้ง `Series` ด้วย `any()` และ `all()`

หากต้องการเอาค่าทั้งหมดของ `Series` มากระทำการ OR กันทุกค่า เช่น `Series` ชื่อ `a` ที่เป็นชนิด `bool` ที่มีสมาชิก `a1`,`a2`,`a3`,`a4` อยู่ 4 ค่า (len=4, ซึ่งแต่ละค่าเป็นแค่ `True/False`) และต้องการหาค่า `a1 OR a2 OR a3 OR a4` จะสามารถทำได้โดยใช้คำสั่ง `Series.any()`

เช่น ต้องการตรวจว่าในคอลัมน์ชื่อ `'day'` มีสักหนึ่งแถวที่มีค่า `Thu` หรือไม่ จะเขียนคำสั่ง ดังนี้

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: ezllt3GS7zHz
outputId: e3a074de-1ce0-4ef7-9d6f-8b33bd08a4f5
---
(tips['day'] == 'Thur').any()
```

+++ {"id": "XBPmzbVI9rJB"}

ซึ่งจะได้จริง เพราะพบอย่างน้อยหนึ่งแถว

หรือในกรณีที่ต้องการหาค่า `a1 AND a2 AND a3 AND a4` ก็ทำได้โดยใช้คำสั่ง `Series.all()`

เช่น ต้องการตรวจว่า ค่าทิปในตาราง มีทิปที่ต่ำกว่า 1 USD หรือไม่ ก็สามารถตรวจโดยเขียนคำสั่ง ดังนี้

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: Y3ebcnZ2-aBe
outputId: b65242be-1976-4f93-f46f-a27772048d8b
---
(tips['tip'] < 1).all()
```

+++ {"id": "SH-wcSZ3-k5Z"}

ซึ่งแสดงว่า ในตารางค่าทิปมีค่าไม่น้อยกว่า 1 USD ทุกค่า

+++ {"id": "wWntwWwLmNh6"}

## **เกี่ยวกับการสร้างคอลัมน์ใหม่**

+++ {"id": "uTJAfMOV4zX3"}

### ต้องการแปลงค่าเงินจากดอลลาร์เป็นบาท

ข้อมูลทิปที่พนักงานเสิร์ฟให้มีค่าทิปและค่าบิลอาหารเป็นหน่วย USD แต่เนื่องจากนักศึกษาอาจอยากทราบเป็นค่าเงินบาท ก็สามารถนำค่าจากคอลัมน์เก่าไปคำนวณ แล้วเก็บในคอลัมน์ใหม่ได้

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: 6Zo99SikUY8a
outputId: 3763138d-5775-4346-eae7-e449473ca87e
---
exchange_rate = 35.0 # สมมติอัตราแลกเปลี่ยนเป็น 1 USD เท่ากับ 35 THB
tips['tip']*exchange_rate   # ค่าอัตราแลกเปลี่ยนถูกคูณเข้าทุก ๆ ค่าของ tip
```

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 206
id: P5E4-Y8bUyAg
outputId: 2750833a-9060-442c-b198-76fd7d4fe09f
---
tips['tip_thb'] = tips['tip']*exchange_rate  # เก็บผลการคำนวณไว้ในคอลัมน์ใหม่ที่ชื่อ tip_thb
tips.head()
```

+++ {"id": "hWFeL_rhVQGt"}

ทั้งนี้ อาจเลี่ยงการสร้างคอลัมน์ใหม่ แต่เก็บผลการคำนวณทับในคอลัมน์เดิมก็ได้ ดังเช่น

`tips['tip'] = tips['tip']*exchange_rate`

แต่ไม่แนะนำให้ทำลักษณะนี้ใน Google Colab เนื่องจากอาจเกิดการอัพเดตทบค่าเทอม หากมีการสั่งให้โค้ดในบรรทัดนี้ทำงานหลายครั้ง

+++ {"id": "P_lFutB5WQ57"}

**ลองทำ:** จงสร้างคอลัมน์ชื่อ `total_bill_thb` ที่เป็นการแปลงค่าเงินจากคอลัมน์ `total_bill` ให้เป็นหน่วยบาท

+++ {"id": "NemKPsS9iu4P"}

### ทิปที่ให้เป็นกี่เปอร์เซนต์ของค่าอาหาร

ที่สหรัฐอเมริกา การให้ค่าทิปจะไม่ถูกรวมอยู่ในบิลอาหาร แต่เป็นการให้ด้วยความสมัครใจ ดังนั้นจึงอยากทราบว่าแต่ละครั้ง ลูกค้าจ่ายบิลกี่เปอร์เซนต์ของค่าอาหาร ซึ่งการคำนวณทำได้ดังนี้

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: DeK3ouZljtQA
outputId: 9e87c638-c431-4acc-e7ab-e3904e673e55
---
tips['tip']/tips['total_bill']    # การนำ Series มาหาร Series จะได้ผลเป็นการนำค่าที่เลข index ตรงกันมาหารกัน
```

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 206
id: UGhcEz8ZkV_9
outputId: 8c2d94b2-2556-44ff-e97c-21f594062a6e
---
tips['%tip'] = tips['tip']/tips['total_bill']*100      # คูณ 100 เพื่อแปลงเป็น %
tips.head()
```

+++ {"id": "njqhcAUhlaX0"}

### ทิปแต่ละวันเป็นกี่เปอร์เซนต์ของทิปทั้งหมด

สมมติว่าพนักงานคนนี้ลาออกจากร้านอาหารนี้แล้ว และเขาอยากทราบว่า ค่าทิปในแต่ละวัน คิดเป็นกี่เปอร์เซนต์ของค่าทิปทั้งหมดที่เขาเคยได้รับมา

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: PSK6BwoQmIgF
outputId: 7963c9d5-eb4f-4127-8c0f-865b7c802adb
---
tips['tip']/tips['tip'].sum()
```

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
id: O7xbLdbMmQ_J
outputId: 6ecd3fda-ec28-4315-ff3f-d902c04cd1fd
---
tips['%tip_of_tips'] = tips['tip']/tips['tip'].sum()*100
tips.head()
```

+++ {"id": "OUALXQwaqSx2"}

**ลองทำ:** จงตรวจสอบว่าคอลัมน์ `%tip_of_tips` มีผลรวมเท่ากับ 1 จริง ๆ หรือไม่

+++ {"id": "MvMFaHBo44jc"}

## **เกี่ยวกับการเรียงลำดับข้อมูล**

การเรียงลำดับจะใช้คำสั่ง `DataFrame.sort_values()` โดยมีพารามิเตอร์ที่สำคัญคือ

- `by` เพื่อระบุว่าให้เรียงโดยใช้ค่าในคอลัมน์ใด
- `ascending` เพื่อระบุว่าให้เรียงจากน้อยไปมากหรือไม่ (default: `True`)

ตัวอย่างของการเรียงข้อมูล เป็นดังนี้

+++ {"id": "3BZIB3F8x0pa"}

### เรียงลำดับข้อมูล `tip` จากน้อยไปมาก

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 300
id: ImsJ_rlXtq2J
outputId: 62b86448-ceb2-4f5e-b94e-043893ad080f
---
sorted_tips = tips.sort_values(by='tip', ascending=True)   # ต้องการเรียงลำดับแถวตามค่า tip จากน้อยไปมาก
sorted_tips.head(8)
```

+++ {"id": "60fRGnZcz10b"}

โดยผลจากการเรียงลำดับ จะเห็นว่าค่า `index` ใน `sorted_tips` มีการสลับลำดับกัน

+++ {"id": "uqJftOctxZi5"}

### เรียงลำดับข้อมูล `tip` และ `total_bill` (ตามลำดับ) จากน้อยไปมาก

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 423
id: f5auMaUOusq_
outputId: 3b977bbc-3cb8-4880-f4fb-ac9a660a6175
---
sorted_tips = tips.sort_values(by=['tip','total_bill'], ascending=True )   # จะเห็นว่าเรียงค่าตาม tip โดยที่ค่า tip เท่ากัน จะเรียงค่า total_bill
sorted_tips
```

+++ {"id": "MusjC9BO2P8-"}

### อยากได้ `index` ที่เรียงลำดับตามค่า `index`

จากตัวแปร `sorted_tips` ที่ค่า `index` สลับที่กันนั้น หากต้องการเรียงลำดับค่า `index` ก็สามารถทำได้ด้วยคำสั่ง `DataFrame.sort_index()`

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 423
id: XagWuQwX3FX3
outputId: 368f6a09-714b-4a88-a1ba-f919219c6b19
---
sorted_tips.sort_index()
```

+++ {"id": "VneQTe8K3u8v"}

### อยากเอา `index` ไปสร้างเป็นคอลัมน์ใหม่

มีความเป็นไปได้ที่จะนำค่า `index` นั้นไปสร้างเป็นคอลัมน์ใหม่ ด้วยคำสั่ง `DataFrame.reset_index()`

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 423
id: jrB60S1y2gE0
outputId: d9a43743-09d9-4ca6-9729-d067daf16808
---
sorted_tips.reset_index()    # จะเห็นว่ามีคอลัมน์ชื่อ index เพิ่มเข้ามา
```

+++ {"id": "0z2N85k25Nxj"}

แต่อย่างไรก็ตาม ถ้าหากไม่ต้องการนำ `index` ไปสร้างเป็นคอลัมน์ใหม่ แต่ให้ลบทิ้งเลย ก็สามาถทำได้ด้วยการเพิ่มพารามิเตอร์ `drop=True`

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 423
id: Q_t5Dw9s5E7o
outputId: a47cbb0e-13d5-4cee-a338-d424b53055e6
---
sorted_tips.reset_index(drop=True)     # ลบลำดับก่อนการเรียงข้อมูลออกไป
```

+++ {"id": "jjJjWb3lyHsJ"}

### ต้องการบันทึก `DataFrame` ลงไฟล์ `csv`

หากต้องการบันทึกตัวแปร `DataFrame` เก็บลงไฟล์ ดังเช่นตัวแปร `sorted_tips` ที่เรียงลำดับค่าไว้แล้ว ก็สามารถทำได้ง่ายด้วย `DataFrame.to_csv()`

ทั้งนี้ กำหนดพารามิเตอร์ `index=False` เพื่อที่จะไม่ต้องบันทึกเลข `index` ลงในไฟล์ `csv` (อย่าลืมว่าเลขนี้ auto generate มาจากตอนอ่านไฟล์ `csv` เข้ามา)

```{code-cell} ipython2
:id: jDwMnqojySHb

# ไฟล์จะถูกเซฟไว้ใน Google Colab (เข้าถึงจากเมนูรูปโฟลเดอร์ด้านซ้ายมือ)
sorted_tips.to_csv('lnwzaa55+.csv', index=False)
```

+++ {"id": "vLxLbp1X0sd-"}

## เกร็ดในการใช้ `Pandas` (Method chaining)

เพื่อความกระชับในการเรียกใช้ฟังก์ชันของ `Pandas` อาจเลือกที่จะเรียกใช้ฟังก์ชันต่อกันเป็นทอด ๆ (Method chaining) โดยไม่ต้องสร้างตัวแปรใหม่ก็ได้ ดังตัวอย่างต่อไปนี้

```{code-cell} ipython2
:id: K9BahlSG1ItP

tips[['total_bill','tip']].sort_values(by='tip', ascending=False).sample(50).agg(['max','min','mean']).to_csv('ggez.csv')
```

+++ {"id": "szAWPUJ261x1"}

**คำถาม:** โค้ดข้างต้นทำอะไร?

+++ {"id": "7xaHDr3t7PXP"}

การเรียกใช้ฟังก์ชันเป็นทอด ๆ ข้างต้น ค่อนข้างที่จะอ่านยาก ดังนั้น ในทางปฏิบัติ อาจใช้วงเล็บมาครอบคำสั่ง เพื่อทำให้สามารถเขียนโค้ดได้ในหลายบรรทัด ดังนี้

```{code-cell} ipython2
:id: OcDs3qzS7sQx

# ข้อสังเกตคือ มีวงเล็บมาครอบ
(tips[['total_bill','tip']]
   .sort_values(by='tip', ascending=False)
   .sample(50, random_state=888)
   .agg(['max','min','mean'])
   .to_csv('ggez.csv')
)
```

+++ {"id": "PvFoJgmM91lL"}

## การวาดกราฟเบื้องต้น

`Pandas` ไม่สามารถวาดกราฟได้ด้วยตัวเอง แต่ช่วยอำนวยความสะดวกการวาดกราฟข้อมูลได้ โดยอาศัยความสามารถของ [`matplotlib`](https://matplotlib.org/), [`Plotly Express`](https://plotly.com/python/plotly-express/) หรือไลบรารีอื่น ๆ ที่ทำงานอยู่เบื้องหลัง (backend)

+++ {"id": "mRF7ZfOKo8vf"}

### การใช้ `Plotly` โดยผ่าน `Pandas`

โดย default แล้ว หากไม่ตั้งค่าอะไร `Pandas` ก็จะใช้ `matplotlib` อย่างไรก็ตาม `plotly` สามารถวาดกราฟได้สวยงามกว่า และมีลูกเล่นมากกว่า ซึ่งหากต้องการใช้ `plotly` เป็นเบื้องหลัง (backend) ในการวาดกราฟ จะต้องกำหนดค่าดังนี้

```{code-cell} ipython2
:id: kkRRKiPbTVm0

pd.options.plotting.backend = "plotly"
```

+++ {"id": "ZXr478dLTYdm"}

การใช้ฟังก์ชันวาดกราฟของ `Pandas` ที่ใช้ backend เป็น `plotly` นั้น เมื่อใช้คำสั่ง `plot()` [(คู่มือ)](https://plotly.com/python/pandas-backend/) ดังนี้

```
DataFrame.plot(x=..., y=..., kind=..., title=..., labels=..., width=..., height=...)
```
ก็จะสามารถวาดกราฟได้หลายชนิด สำหรับรายละเอียดเบื้องต้นของค่าพารามิเตอร์ของฟังก์ชัน  แสดงดังตารางต่อไปนี้

|พารามิเตอร์ | ค่า | ความหมาย|
|:---|:---|:---|
| `x=` | `str` | ชื่อคอลัมน์ของข้อมูลแกนนอน |
| `y=` | `str` | ชื่อคอลัมน์ของข้อมูลพิกัดแกนตั้ง  |
| `color=` | `str` | ชื่อคอลัมน์ที่ใช้จัดกลุ่มสี |
| `kind=`| `'line'` | line plot (default)|
|| `'bar'` | bar plot|
|| `'hist'` | histogram|
|| `'scatter'` | scatter plot |
|`title=` | `str` | ชื่อกราฟ|
|`labels=`| `dict()` | กำหนดชื่อแกน |
| `width=` | `int` | ความกว้างของกราฟ |
| `height=` | `int` | ความสูงของกราฟ |

ค่าอื่น ๆ ที่เป็นไปได้ สำหรับ `kind=` ของ `plotly` backend คือ `'box'`,`'area'`,`'violin'`, `'strip'`, `'funnel'`, `'density_heatmap'`, `'density_contour'`

ทั้งนี้ กรณีเลือก `matplotlib` เป็น backend ก็อาจมีค่าพารามิเตอร์บางตัว แตกต่างจากนี้

+++ {"id": "q2xAob7NqdAG"}

#### Bar chart

ตัวอย่างต่อไปนี้เป็นการวาดกราฟแท่งที่มีแกนนอนคือ `day` และความสูงคือ `total_bill`

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 542
id: Zp-nvzrPOlPP
outputId: c640da9d-b3a0-4afe-f94e-de089e3afb37
---
tips.plot(x="day", y="total_bill", kind='bar')
```

+++ {"id": "xw7ik9BmRS9C"}

สามารถเพิ่มเติมค่า `color` เพื่อให้แยกสีตามค่า `sex`

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 542
id: zPQJA7seqcN6
outputId: 648513cc-adac-4eac-d8e7-12ad9153fe91
---
tips.plot(x="day", y="total_bill", color="sex", kind='bar')
```

+++ {"id": "p1bUvGSTg0Sc"}

การกำหนด `color='sex'` จะได้กราฟที่แต่ละแท่งซ้อนกัน เรียกว่า stacked bar chart ซึ่งสามารถแยกแต่ละแท่งให้เป็นแท่งเดียว ด้วยการกำหนด `barmode='group'` ดังนี้

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 542
id: 5fB--2CsgqrI
outputId: 18e537d8-70b3-4228-f09e-de03da59e0ec
---
tips.plot(x="day", y="total_bill", color="sex", kind='bar', barmode='group')
```

+++ {"id": "Nz2SWuXwRb8w"}

**ลองทำ**
- ลองเพิ่มพารามิเตอร์ `orientation='h'` พร้อมสลับค่าของ `x=` และ `y=` จะได้กราฟอะไร
- ลองเปลี่ยนเป็น `kind='hist'` จะได้กราฟอะไร? แล้ว `kind='bar'` และ `kind='hist'` ต่างกันอย่างไร?

+++ {"id": "y8ecnpvezoE7"}

#### Histogram

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 542
id: Ok9lGDY5zrWY
outputId: 58eb0e31-1f28-4118-98e0-bb4536941af1
---
tips.plot(x="%tip", kind='hist', nbins=40, text_auto=True)
```

+++ {"id": "DfjFoYzlVLq9"}

**ลองทำ** ลองปรับค่า `nbins`

+++ {"id": "8LmWBjqrf-oH"}

#### Scatter plot

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 417
id: sMrCNR7-XsiF
outputId: 770e5761-a204-4e91-e6d1-c8a50079e072
---
fig = tips.plot(x='total_bill', y='%tip',
          color='time',   # กำหนดสีแต่ละจุดตามค่า time
          kind='scatter', # ชนิดกราฟ
          title='กราฟแสดงทิปที่ได้ในแต่ละครั้ง',
          labels={'%tip': 'สัดส่วนการให้ทิป (%)','total_bill':'ค่าบิลอาหาร (USD)'},  # กำหนด dictionary ในการตั้งชื่อแกนนอนและแกนตั้ง
          width=800, height=400,  # ขนาดของรูป
)
fig.update_layout(margin_t=40)  # แก้ไขระยะระหว่าง title กับกราฟ
fig.show()
```

+++ {"id": "jHJL-dkZVYyo"}

### การใช้ `Plotly` โดยตรง

`plotly` backend สำหรับ `Pandas` เป็นคุณสมบัติใหม่ที่เพิ่งมีใน `Pandas` และยังไม่สมบูรณ์ ดังนั้น การใช้งานจึงมีข้อจำกัด ดังนั้น ในหลายกรณีจึงมีความจำเป็นที่จะต้องวาดกราฟโดยเรียกใช้  `plotly` โดยตรง ซึ่งทำได้โดยการนำเข้า `plotly` ด้วยคำสั่ง ดังนี้

```
import plotly.express as px
```

และแทนที่จะใช้คำสั่ง `plot()` ในการวาดกราฟแต่ละชนิด แต่จะใช้คำสั่งต่อไปนี้

| ฟังก์ชัน | ชนิดกราฟ |
|:---|:---|
| `px.bar(data, x=..., y=...)` | กราฟแท่ง (หาก `orientation='h'`) จะได้กราฟแท่งแนวนอน |
| `px.scatter(data, x=..., y=...)` | scatter plot  |
| `px.histogram(data, x=...)` | histogram |

ซึ่งยกตัวอย่างการสร้างกราฟแท่ง ได้แก่

```{code-cell} ipython2
---
colab:
  base_uri: https://localhost:8080/
  height: 542
id: L4dSvRwXVdRp
outputId: cd89aaf3-d2e9-479c-bac5-e1c415875cd3
---
import plotly.express as px
px.bar(tips, x="day", y="total_bill")
```

+++ {"id": "DZidxjgXXwEe"}

จะเห็นว่ากราฟที่ได้ เหมือนกับการวาดกราฟโดยเรียกใช้ฟังก์ชัน `plot()` จาก `Pandas`

**ลองทำ**

- กราฟที่เคยวาดโดยใช้ฟังก์ชัน `plot()` ของ `Pandas` จงวาดกราฟแบบเดิม แต่เปลี่ยนไปใช้คำสั่ง `px.bar()`, `px.scatter()` และ `px.histogram()`

+++ {"id": "OfBzKQFYX_XH"}

### ศึกษาตัวอย่างการวาดกราฟด้วยตนเอง

เนื่องจากการวาดกราฟมีรูปแบบมากมาย นักศึกษาอาจศึกษาการวาดกราฟจากการดูตัวอย่างและคู่มือของ `plotly` ซึ่งขอให้ไว้ตามรายการต่อไปนี้

1. [การใช้ `plotly` เป็น backend ของ `Pandas`](https://plotly.com/python/pandas-backend/)
2. [ตัวอย่างการใช้ `plotly`](https://plotly.com/python/plotly-express/)
  - [ตัวอย่างการสร้าง bar chart](https://plotly.com/python/bar-charts/) และ [คู่มือ](https://plotly.com/python-api-reference/generated/plotly.express.bar)
  - [ตัวอย่างการสร้าง histogram](https://plotly.com/python/histograms/) และ [คู่มือ](https://plotly.com/python-api-reference/generated/plotly.express.histogram)
  - [ตัวอย่างการสร้าง scatter plot](https://plotly.com/python/line-and-scatter/) และ [คู่มือ](https://plotly.com/python-api-reference/generated/plotly.express.scatter)


*หมายเหตุ:* อาจดู[คู่มือการใช้ฟังก์ชัน `plot()` ของ `Pandas`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.plot.html) แต่บางพารามิเตอร์อาจใช้ไม่ได้ เนื่องจากเป็นคู่มือสำหรับ backend ที่เป็น `matplotlib`

+++ {"id": "vmWy0IN_aRjR"}

**จบเนื้อหา**

นักศึกษาลองสรุปซิว่า วันนี้นักศึกษาได้เรียนรู้คำสั่งอะไรบ้าง
