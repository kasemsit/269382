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
  name: python3
---

+++ {"id": "GbkMkzKH9lEy"}

# สำรวจชุดข้อมูลขายของออนไลน์

**จุดประสงค์การเรียนรู้**
1. การอ่านไฟล์ Excel และการนำข้อมูลตารางมาต่อกัน
2. การตรวจสอบความไม่สอดคล้องของข้อมูล
3. การตรวจสอบและจัดการข้อมูลที่ขาดหาย (Missing values)
4. คำนวณภาพรวมของข้อมูลเป็นกลุ่ม (`groupby`)
5. จัดการข้อมูลเกี่ยวกับเวลา
6. เรียนรู้การวาดกราฟเพิ่มเติมจากคาบที่ผ่านมา

+++ {"id": "vSdsS2E5KS4U"}

## เริ่มต้นบทเรียน

ร้านขายของออนไลน์แห่งหนึ่งได้บันทึกรายการธุรกรรม (transaction) ระหว่างวันที่ 1 กรกฎาคม 2011 ถึง 31 สิงหาคม 2011 ร้านค้ารายนี้จดทะเบียนในสหราชอาณาจักร ขายของใช้เก๋ ๆ ไม่ซ้ำใคร และถึงแม้จะไม่มีหน้าร้าน แต่กลุ่มลูกค้าก็เข้าถึงจากหลากหลายประเทศ

รายละเอียดของแต่ละรายการธุรกรรม มีดังนี้

| คอลัมน์ | คำอธิบาย |
| :-- | :-- |
| `InvoiceNo` | เลขธุรกรรม (ตัวเลข 6 หลัก) โดยหากมีการขึ้นต้นด้วย `C` จะหมายถึงการยกเลิกสินค้า |
| `StockCode` | รหัสสินค้า (ตัวเลข 5 หลัก) |
| `Description` | ชื่อสินค้า |
| `Quantity` | จำนวนชิ้นที่ซื้อ  |
| `InvoiceDate` | วันและเวลาของธุรกรรม  |
| `UnitPrice` | ราคาต่อหน่วย |
| `CustomerID` | รหัสลูกค้า (ตัวเลข 5 หลัก) |
| `Country` | ประเทศที่อยู่ของลูกค้า |



+++ {"id": "7YKIocQAIiYX"}

## ดาวน์โหลดข้อมูล

ในขั้นแรก จะดาวน์โหลดข้อมูลและบันทึกไว้ในไฟล์ชื่อ `data.xlsx`

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: 3bYVDa8Np9SR
outputId: 0139963d-68a7-43fb-c408-8eb4a6315698
---
# ใช้คำสั่ง wget ซึ่งเป็นคำสั่ง linux (ไม่ใช่โค้ดภาษา Python) ใน
!wget -c https://github.com/kasemsit/269382/raw/main/dataset/online_retail_2months.xlsx -O data.xlsx
```

+++ {"id": "ymsqpnbOFK4g"}

**คำอธิบาย:** โค้ด `!wget` ข้างต้นไม่ใช่ภาษา Python แต่เป็นการเรียกใช้โปรแกรม `wget` ที่เป็นโปรแกรมของระบบปฏิบัติการ Linux ผ่านทาง command line ดังสังเกตุได้จากเครื่องหมาย `!` นำหน้า ที่เป็นการบอกให้ Google Colab เรียกโปรแกรม `wget` โดยสิ่งที่ตามมา มีความหมายคือ
- `-c` หมายถึงให้ดาวน์โหลดแบบ resume (คือไม่ต้องดาวน์โหลดใหม่ถ้ามีไฟล์อยู่แล้ว)
- `https://github.com/kasemsit/269382/raw/main/dataset/online_retail_2months.xlsx` คือ URL ของไฟล์
- `-O data.xlsx` หมายถึง ให้ดาวน์โหลดแล้วบันทึกไฟล์ในชื่อ `data.xlsx`

นอกจากนี้ นักศึกษาสามารถเรียกใช้โปรแกรมอื่น ๆ นอกจาก `wget` ได้เช่น `!ls` เพื่อดูว่าโฟลเดอร์ปัจจุบันมีไฟล์อะไรบ้าง หรือแม้กระทั่ง `!unzip ชื่อไฟล์` เพื่อทำการแตกไฟล์ zip เป็นต้น

+++ {"id": "3cUd1psdLVBc"}

**ลองทำ:**
1. ดาวน์โหลดไฟล์ Excel ไปที่คอมพิวเตอร์ของนักศึกษาด้วย และอ่านไฟล์ด้วยโปรแกรม Excel
2. ไฟล์ Excel ที่เก็บข้อมูล มีกี่ Sheet และชื่อ Sheet อะไรบ้าง

ในขั้นตอนต่อจากนี้ จะเป็นการอ่านไฟล์ Excel ใน Google Colab ด้วย `Pandas`

+++ {"id": "OrX0AcAe4rD-"}

## อ่านข้อมูลจากไฟล์ Excel

เมื่อดาวน์โหลดข้อมูลสำเร็จและบันทึกไว้ในไฟล์ `data.xlsx` จากนั้นจึงอ่านไฟล์เข้ามาด้วยคำสั่ง `read_excel()` ของ `Pandas` [(ดูคู่มือ)](https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html) ซึ่งมีรูปแบบ ดังนี้

```python
pd.read_excel(ชื่อไฟล์, sheet_name=..., header=..., skiprows=...)
```

โดยที่พารามิเตอร์ที่สำคัญที่ใช้บ่อย ได้แก่

| พารามิเตอร์  | การกำหนดค่า | ค่า default |
|:---|:---|:--|
|`sheet_name`| ชื่อ sheet ที่ต้องการอ่าน หรือตัวเลขลำดับที่ของ sheet |  `0` (sheet แรก) |
| `skiprows` | เลขแถวที่จะให้เริ่มอ่านเป็นแถวแรก (แถวแรกนับเป็นแถวที่ `0`) | `0` (แถวแรกของ sheet) |
| `header` | ให้ระบุ `header=None` หากไม่มีชื่อคอลัมน์ใน sheet  | `0` (แถวแรกของ sheet เป็น `header`) |
| `nrows` | จำนวนแถวที่ต้องการอ่าน (นับจาก `header`) | `None` (อ่านทุกแถวจนจบ sheet) |

+++ {"id": "IOxFuPvPMkMO"}

#### อ่าน Sheet เดือนกรกฏาคม

```{code-cell}
:id: hbXLYrO6aZCl

# บรรทัดนี้ไม่ใช่คำสั่ง Python แต่เป็นคำสั่งพิเศษ (magic command) ของ Google Colab (หรือ iPython) ที่ใช้เคลียร์ตัวแปรในหน่วยความจำ
%reset -f
```

```{code-cell}
:id: djuDDiGQMnq1

import pandas as pd
data_jul = pd.read_excel('data.xlsx',
                      sheet_name='July',  # เดือนกรกฎาคม
                      skiprows=3,
                      )
```

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 174
id: HrQ8d4-MOE9C
outputId: 3e3a10ef-6f08-4809-bce8-86ac3168399c
---
data_jul.head(4)
```

+++ {"id": "Rp3Hc5rvMf-Z"}

#### อ่าน Sheet เดือนสิงหาคม

```{code-cell}
:id: _mZdpqRkelO9

import pandas as pd
data_aug = pd.read_excel('data.xlsx',
                      sheet_name='August',  # เดือนสิงหาคม
                      skiprows=3,
                      )
```

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 174
id: rzFI55qQOJME
outputId: 6d12a646-be62-4059-a481-6395cee56abe
---
data_aug.head(4)
```

+++ {"id": "cm7GeFr_WUQ6"}

## Q1. ต้องการนำตารางมาต่อกัน

สำหรับเนื้อหาในวันนี้ จะพิจารณาข้อมูลทั้ง 2 เดือน ดังนั้นจึงจำเป็นที่ต้องนำตัวแปร `data_jul` และ `data_aug` มาต่อกัน (concatenation)

+++ {"id": "MZuSHo6zWpcT"}

### Q1.1 การเพิ่มคอลัมน์ที่เก็บค่าเดียวเหมือนกันหมด

ก่อนที่จะนำตารางมาต่อกัน เราจะเพิ่มคอลัมน์ที่ระบุว่า แต่ละตารางมาจาก Sheet ไหน ดังนี้

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 206
id: k8vHoipgW9Kq
outputId: f156d72d-1c00-47ea-d602-fdf6190f40c2
---
data_jul['Sheet'] = 'July'    # สร้างคอลัมน์ใหม่ชื่อ Sheet ใน data_jul ที่มีค่าเท่ากับ July ทั้งหมด
data_aug['Sheet'] = 'August'  # สร้างคอลัมน์ใหม่ชื่อ Sheet ใน data_aug ที่มีค่าเท่ากับ August ทั้งหมด
data_aug.head()
```

+++ {"id": "cI-6w07ON7AT"}

### Q1.2 การนำตารางมาต่อกัน

การนำตารางมาต่อกัน ทำได้ด้วยคำสั่ง `pd.concat()` ซึ่งมีรูปแบบการใช้ ดังนี้

```python
new_data = pd.concat( tuple_ที่เก็บตัวแปรตาราง )
```

เช่น หากมีตาราง `A`, `B` และ `C` ที่ต้องการนำมาต่อกันตามลำดับ ก็ให้กำหนด `tuple_ที่เก็บตัวแปรตาราง = (A, B, C)` เป็นต้น โดย `Pandas` จะทำการนำคอลัมน์ของ  `A`, `B` และ `C` ที่ชื่อเหมือนกัน มาต่อกัน (ซึ่งหมายความว่า หากในตาราง มีลำดับคอลัมน์ไม่เหมือนกัน แต่ชื่อคอลัมน์ตรงกัน ตารางก็จะยังสามารถนำมาต่อกันได้อย่างถูกต้อง)

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 174
id: 6O5-OCaxMKHj
outputId: baf0afcd-a182-4a3d-944d-71bd91c0d7f4
---
data = pd.concat( (data_jul, data_aug))   # ต้องการเอา `data_aug` มาต่อท้าย `data_jul`
data.sample(4)
```

+++ {"id": "aQvRjmJoLHo7"}

สำหรับข้อมูลในวันนี้ ทั้ง `data_jul` และ `data_aug`  มีชื่อคอลัมน์เหมือนกัน จึงสามารถนำมาต่อกันได้โดยง่าย

อย่างไรก็ตาม `DataFrame` ที่ได้จากการต่อตาราง จะมี `index` ที่ซ้ำกัน เพราะว่า `index` ของทั้ง `data_jul` และ `data_aug` ต่างเริ่มนับจาก `0` ปัญหานี้ สามารถตรวจสอบได้ เช่น

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 112
id: 3kU5hAN4TgyA
outputId: ae01ab6d-6bbb-4dd4-a0b5-4a4d2e375daa
---
data[data.index == 555]  # พิมพ์แถวที่มี index เท่ากับ 555 ออกมา ซึ่งจะพบว่ามีซ้ำกัน 2 แถว (แต่ละแถวมาจากแต่ละ Sheet)
```

+++ {"id": "2npVBkbZUsCJ"}

การที่ `index` มีค่าซ้ำกัน อาจทำให้เกิดความผิดพลาดในการคำนวณในอนาคต ดังนั้น หากไม่ต้องการให้ `pd.concat()` ใช้ `index` เดิม (ซึ่งสร้างอัตโนมัติมา) แต่ให้สร้าง `index` ใหม่ ก็ทำได้ด้วยการเพิ่มพารามิเตอร์ `ignore_index=True`

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 80
id: Ij_hMOnQVMOc
outputId: 61e56a4f-4ecc-4c8a-fa78-c1e14c9c3717
---
data = pd.concat( (data_jul, data_aug), ignore_index=True)
data[data.index == 555]   # คราวนี้จะเห็นว่า index เท่ากับ 555 มีแถวเดียว
```

+++ {"id": "doNJeyDrVyuH"}

**ลองทำ:**

- `ignore_index=True` ทำให้สูญเสีย `index` ของข้อมูลเดิม ซึ่งอาจเป็นปัญหาในกรณีที่ต้องการเข้าถึงค่า `index` เดิม ดังนั้น หากต้องการเก็บค่า `index` เดิมไว้ จะต้องทำอย่างไร (ใช้ความรู้จากคาบก่อน)

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 174
id: 8ShZZx3ILfz6
outputId: f48ad7d7-175a-4e17-ae3b-efe8c7265bf4
---
# เฉลย
data_jul_reset_index = data_jul.reset_index()  # จะมีคอลัมน์ชื่อ index เพิ่มเข้ามา
data_aug_reset_index = data_aug.reset_index()
data = pd.concat( (data_jul_reset_index, data_aug_reset_index), ignore_index=True)
data.sample(4)
```

+++ {"id": "0Kj15YZM76IT"}

## Q1.3 การลบคอลัมน์

สมมติว่า ไม่ต้องการใช้คอลัมน์ `Sheet` ทีสร้างขึ้นอีกแล้ว และอยากจะลบออกจาก `DataFrame` เลย จะลบได้โดยใช้ฟังก์ชัน

```
DataFrame.drop(columns=...)
```
โดยที่ `columns` คือชื่อคอลัมน์หรือรายการชื่อคอลัมน์ที่ต้องการลบ

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 423
id: DAsq7lNm803j
outputId: 2a07c422-257a-4403-f971-c18ab03fe960
---
data.drop(columns=['Sheet']) # จะเห็นว่าผลลัพธ์ที่ได้ คอลัมน์ Sheet หายไป
```

+++ {"id": "EKfbNJRs9I5K"}

## เกร็ดการใช้ `Pandas` (`inplace=True`)

ฟังก์ชันที่แก้ไข `DataFrame`อย่างเช่นฟังก์ชัน `DataFrame.drop()` ฯลฯ มันไม่เขียนทับต้นฉบับเดิม ดังนั้นเวลาจะนำไปใช้ต่อ จึงต้อง assign ค่าให้ตัวแปรใหม่ หรือหากต้องการเขียนทับตัวแปรเดิม ในตัวอย่างก่อนหน้า ก็จะต้องเขียนว่า
```python
 data = data.drop(columns=['Sheet'])   # แบบที่ 1
```

หรืออีกทางเลือกหนึ่ง ซึ่ง `Pandas`  อำนวยความสะดวกให้ในกรณีที่ต้องการเขียนทับต้นฉบับ คือการกำหนดพารามิเตอร์ `inplace=True` ดังนี้
```python
 data.drop(columns=['Sheet'], inplace=True)   # แบบที่ 2
```

ซึ่งหากเขียนแบบนี้แล้ว ก็ไม่ต้องนำตัวแปรมารับค่าอีก ซึ่งหากทำดังโค้ดต่อไปนี้ ก็จะเกิดข้อผิดพลาด นำตัวแปร `data` ไปใช่ต่อไปไม่ได้
```python
# ผิดพลาด!! ทำแบบนี้แล้ว data ที่ได้จะเป็นค่า None
 data = data.drop(columns=['Sheet'], inplace=True)  
 print(data)  # จะได้ None
```
สาเหตุที่เป็นเช่นนี้ก็เพราะ
- `inplace=False` ทำให้ฟังก์ชัน `return` ตัวแปรที่ผ่านการแก้ไข แต่ต้นฉบับเดิมยังไม่เปลี่ยน
- `inplace=True` ทำให้ฟังก์ชันแก้ตัวแปรต้นฉบับ พร้อมกับ `return` ค่า `None`

**คำแนะนำ**
- เลือกใช้ตามความเหมาะสม

+++ {"id": "dqk6z45vMBCA"}

## Q2 ตรวจสอบข้อมูล `Quantity` และ `UnitPrice`

เนื่องจากข้อมูลที่ได้รับมา อาจมีความไม่ถูกต้องในข้อมูลอยู่ด้วย ยกตัวอย่างเช่น หากลองสุ่มแถวมาดูเรื่อย ๆ จะพบสิ่งผิดปกติ  บางแถวมี `Quantity` ติดลบ หรือแม้กระทั่ง `UnitPrice` ติดลบ ซึ่งเราไม่ทราบว่ามีที่มาอย่างไร ดังนี้ เราจะลองเข้าไปดูหัวข้อนี้

+++ {"id": "5bpMSkXHrK0C"}

### Q2.1 มี `Quantity` น้อยกว่า `0 ` หรือ `UnitPrice` น้อยกว่า `0` หรือไม่

ก่อนอื่น จะสุ่มพิมพ์แถวที่มี `'Quantity' < 0` จะพบว่ามี `Quantity` ติดลบอยู่จริง

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 206
id: 9Vx26a5Adwpj
outputId: affad475-9de9-4cb6-e29d-7f49228a3336
---
data[data['Quantity'] < 0].sample(5)    # Quantity < 0 ได้อย่างไร?
```

+++ {"id": "a0XDV_ENqvLR"}

**ลองทำ:** จงหาว่า `'UnitPrice'` ที่เป็นลบ มาทั้งหมดกี่แถว

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 112
id: tzOjNx4vxxd_
outputId: 971a951e-efdc-4076-ed31-d783354f41d3
---
# เฉลย
data[data['UnitPrice'] < 0] # จะเห็น InvoiceNo มีตัว A นำหน้าด้วย
```

+++ {"id": "UyMp9Z0ZNHpF"}

### Q2.2 `InvoiceNo` กับ `Quantity` และ `UnitPrice`

จากผลการพิมพ์แถวที่มี `'UnitPrice' < 0`จะพบความผิดปกติของข้อมูลที่ไม่สอดคล้องกับคำอธิบายข้อมูล (Data dictionary) ที่ผู้แจกจ่ายข้อมูลให้มา นี่เป็นปัญหาปกติที่ต้องเผชิญอย่างหลีกเลี่ยงไม่ได้ ก่อนที่จะสามารถทำข้อมูลไปใช้ประโยชน์ได้

Data dictionary บอกทราบว่า `InvoiceNo` เป็นเลข 6 หลัก ที่หากขึ้นต้นด้วย `'C'` จะหมายถึงการยกเลิกสินค้า แต่จากการพิมพ์แถวที่ `'UnitPrice' < 0`จะพบ  `InvoiceNo` ขึ้นต้นด้วย `'A'` ด้วย ดังนั้นในหัวข้อนี้จะเจาะลึกคอลัมน์ `InvoiceNo`


**คำถามที่ต้องการตอบ**

1. จะเข้าถึงแถวที่ค่าในคอลัมน์ `InvoiceNo` ขึ้นต้นด้วย `C` หรือ `A` ได้อย่างไร
2. ถ้า `InvoiceNo` ขึ้นต้นด้วย `C` แล้ว `Quantity` น้อยกว่า `0` เสมอ?

เพื่อที่จะได้คำตอบ จะทำเป็นขั้น ๆ ดังนี้

+++ {"id": "IRMN2etHyNM4"}

#### **1) การเข้าถึงแถวที่ค่าในคอลัมน์ `InvoiceNo` ขึ้นต้นด้วย `C` หรือ `A`**

+++ {"id": "0PliJzVXN74R"}

***ตรวจสอบว่าคอลัมน์ `InvoiceNo` เก็บข้อมูลชนิดใด***


```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: UwFn0_WwPUmX
outputId: 9d9dc836-e540-49c5-b053-1b15615e0984
---
data['InvoiceNo'].dtype    # จะใช้คำสั่ง data.info() จากคาบก่อนเพื่อตรวจดูก็ได้
```

+++ {"id": "gfLJuZAZPisj"}

จะเห็นว่า เป็นชนิดแบบผสม (`dtype('O')` คือ `object`)

**แปลงชนิดข้อมูลของคอลัมน์ `InvoiceNo`**

การที่ข้อมูล `InvoiceNo` เป็นชนิด `object` จะยากแก่การตรวจสอบว่า แต่ละค่าขึ้นต้นด้วยอักษร `C` หรือไม่ ดังนั้นจึงจะแปลงชนิดข้อมูลในคอลัมน์นี้ ให้เป็นชนิด `string` เสียก่อน ด้วยคำสั่ง `Series.astype('string')` ดังนี้

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: 7l0ohSxaQXHp
outputId: 16e56cc5-7424-4c0c-8c64-e0157d872889
---
# หมายเหตุ: คอลัมน์อื่น ๆ ที่จำเป็นต้องแปลงข้อมูลให้ถูกต้องก็มีอีกหลายคอลัมน์ แต่ขอข้ามไปก่อน
data['InvoiceNo'] = data['InvoiceNo'].astype('string')  # แปลงแล้วเขียนทับลงคอลัมน์เดิม
data['InvoiceNo'].dtype
```

+++ {"id": "_XSqD7aWQy69"}

**ตรวจสอบว่า `InvoiceNo` ขึ้นต้นด้วย `C` หรือไม่**

เมื่อคอลัมน์ `InvoiceNo` ถูกแปลงเป็นชนิด `string` แล้ว จะสามารถใช้ฟังก์ชันเกี่ยวกับ `string` ของ `Pandas` ได้อย่างอิสระ

การจะเข้าถึงสมาชิกแต่ละตัวของ `Series` ที่เก็บ `string` ได้นั้น จะต้องกระทำผ่านตัวช่วยที่เรียกว่า **String method** (`.str`) ดังรูปแบบ ต่อไปนี้
```python
Series.str.ฟังก์ชันสตริง
```

ซึ่งตัวอย่างของฟังก์ชัน ได้แก่

| ฟังก์ชันสตริง  | ตัวอย่างการใช้งาน |  คำอธิบาย |
|:---|:---|:--|
|`startswith()` |`Series.str.startswith('H')` | เช็คว่าอักษรตัวแรกเป็น `H` หรือไม่ |
|`endswith()` |`Series.str.endswith('y')` |  เช็คว่าอักษรตัวสุดท้ายเป็น `y` หรือไม่ |
|`lstrip()` |`Series.str.lstrip('ah')` | ไล่ลบตัวอักษร `a` หรือ `h` โดยเริ่มลบจากทางซ้ายไปขวา และลบจนกว่าจะเจออักษรที่ไม่ใช่ `a` หรือ `h`   |
| |`Series.str.lstrip()`   | ลบช่องว่างด้านซ้าย |
|`rstrip()` | `Series.str.rstrip()`|   คล้าย `lstrip()` แต่ไล่ลบเริ่มจากด้านขวา  |
|`strip()` |`Series.str.strip()` |  กระทำทั้ง `lstrip()` และ `rstrip()`  |
|`len()` |`Series.str.len()` |  นับจำนวนตัวอักษร  |

สำหรับตัวอย่างการใช้งาน String method ของ `Pandas` อื่น ๆ ศึกษาเพิ่มเติมได้จาก [ลิงค์](https://pandas.pydata.org/docs/user_guide/text.html#string-methods) และ[ตารางสรุปฟังก์ชัน](https://pandas.pydata.org/docs/user_guide/text.html#method-summary)


+++ {"id": "mgp7m0s_cnax"}

ในกรณีนี้ เราต้องการตรวจสอบว่า `InvoiceNo` ขึ้นต้นด้วยอักษร `C` หรือไม่ จึงใช้ `startswith()` ดังนี้

```{code-cell}
:id: 7xTpcSIHkXl1

flag_c = data['InvoiceNo'].str.startswith('C')  # True คือขึ้นต้นด้วย C ส่วน False ไม่ขึ้นต้นด้วย C
```

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 223
id: uun4-MB9OjlI
outputId: 6dc7798d-99b4-4dfc-b913-e8c6cba88b42
---
data_c = data[flag_c]
print(f'Invoice ขึ้นต้นด้วย C มี {len(data_c)} แถว')
data_c.sample(5)
```

+++ {"id": "K_ztuohAzSRq"}

และในลักษณะเดียวกัน สามารถเข้าถึงแถวที่ขึ้นต้นด้วย `'A'`

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 160
id: nXpDy1aGzell
outputId: c0246a94-0a19-4d06-c2e4-2c4a3f926aa0
---
flag_a = data['InvoiceNo'].str.startswith('A')
data_a = data[flag_a]
print(f'Invoice ขึ้นต้นด้วย A มี {len(data_a)} แถว')
data_a
```

+++ {"id": "DGo7pmeelf9T"}

#### 2) ถ้า `InvoiceNo` ขึ้นต้นด้วย `C` แล้ว `Quantity` ติดลบเสมอ?

นับจำนวนแถวของ `InvoiceNo` ที่เป็นการยกเลิก และมี `Quantity` น้อยกว่า `0`

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: ZLjlex4_gjsx
outputId: 97dcd994-33a9-40c3-e9ac-09933702eb38
---
flags = (data_c['Quantity'] < 0) # ในบรรดา Invoice ที่ขึ้นต้นด้วย C
len(data_c[flags])    # Invoice ขึ้นต้นด้วย C และ Quantity < 0 มี 1353 แถว ซึ่งเท่ากับจำนวนแถวทั้งหมดของ data_c
```

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: HBk9dQTfiVAR
outputId: 3fa60742-8042-4670-da77-0379ce1a9988
---
flags = (data_c['Quantity'] > 0)
len(data_c[flags])   # ไม่มี Invoice ขึ้นต้นด้วย C ที่มี Quantity > 0
```

+++ {"id": "wHbize0cm6mB"}

ดังนั้นจากข้อมูลที่มี จึงสรุปได้ว่า ถ้า `InvoiceNo` ขึ้นต้นด้วย `C` แล้ว `Quantity` จะน้อยกว่า `0` เสมอ

+++ {"id": "9rIpQeGwyn2C"}

นอกจากนี้ เรายังพบอีกว่า คอลัมน์ `Quantity` ไม่มีค่าที่เท่ากับ `0` เลย

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: vyYgmrXPgv1L
outputId: 2cbecfb6-328a-4807-9795-24e1ffb0c0a2
---
flags = (data['Quantity'] == 0) # เช็คข้อมูลทั้งหมด
len(data[flags])   # ไม่พบว่าในชุดข้อมูลทั้งหมดมีการบันทึกค่า Quantity == 0
```

+++ {"id": "F9tFHlxSnIjL"}

#### **แบบฝึกหัด**

จงเติมตารางต่อไปนี้ให้สมบูรณ์ (ช่องที่เป็นเครื่องหมาย `?` เป็นค่าอะไร)

*หมายเหตุ:* เราทราบก่อนหน้าแล้วว่า `Quantity` ไม่เคยเท่ากับ `0`

+++ {"id": "As9XMCL-iEY-"}

| `InvoiceNo`  | `Quantity` | `UnitPrice` | จำนวนแถว | สมมติฐาน |
|:--|:--|:--|--:| :--|   
| `C` | `> 0`| `> 0` | 0 | |
| `C` | `> 0`| `== 0` | 0 | |
| `C` | `> 0` | `< 0` | 0 | |
| `C` | `< 0` | `> 0` | 1353 |  การคืนสินค้า จะใส่ `Quantity` ติดลบ  แต่ `UnitPrice` อาจจะเป็น `UnitPrice` ที่ซื้อไป จึงเป็นบวก |
| `C` | `< 0` | `== 0` | 0 |  |
| `C` | `< 0` | `< 0` | 0 | |
| not `C` |`> 0` |`> 0` | 73128 | รายการขายออกไป จึงมีแต่ค่าบวก (แต่มีรายการที่ `InvoiceNo` ขึ้นต้นด้วย `A` อยู่ 1 รายการ ) |
| not `C` |`> 0` |`== 0` |  **?** | หลากหลายเหตุผลที่ไม่อาจทราบได้ เช่นอาจเป็นสินค้าที่คิดว่าเสียหาย แต่เพิ่งเจอใน stock, อาจลงเลขผิด ฯลฯ  |
| not `C` |`> 0` |`< 0` | 2 | รายการที่ `InvoiceNo` ขึ้นต้นด้วย `A` |
| not `C` |`< 0` |`> 0` | 0 | |
| not `C` |`< 0` |`== 0` | **?**   | หลากหลายเหตุผลที่ไม่อาจทราบได้ เช่นอาจเป็นสินค้าที่เสียหาย ที่ไม่ได้ขายออกไป, อาจลงเลขผิด ฯลฯ  |
| not `C` |`< 0` |`< 0` | 0 | |
| | | รวม | 74802 | |

  
  

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: 6gau4oFSnXWS
outputId: 8f378917-b07c-4eab-a718-7c0dfcd2c15b
---
# เฉลย
ans1 = len(data[~data['InvoiceNo'].str.startswith('C') & (data['Quantity'] > 0) & (data['UnitPrice'] == 0)])
ans2 = len(data[~data['InvoiceNo'].str.startswith('C') & (data['Quantity'] < 0) & (data['UnitPrice'] == 0)])
print(f'คำตอบคือ {ans1} กับ {ans2} ตามลำดับ')
```

+++ {"id": "HiTuPv2j6IcR"}

## Q2 การแปลงชนิดข้อมูลให้ถูกประเภท

ข้อมูลแต่ละคอลัมน์ใน `DataFrame` ถูกกำหนดชนิดข้อมูลโดยอัตโนมัติ ซึ่งอาจมีความผิดพลาดได้ ดังนั้น จึงเป็นหน้าที่ของนักวิเคราห์ข้อมูลที่จำต้องกำหนดให้ถูกต้องแต่เนิ่น ๆ

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: 0r-q61Wh7Ylj
outputId: c5caea6f-5ded-4708-f6ee-e3dfaaa60ea2
---
data.info()
```

+++ {"id": "slHkFVo67bWf"}

จาก `data.info()` จะพบว่า `InvoiceNo` ถูกแปลงไว้ถูกต้องแล้วจากหัวข้อที่แล้ว

ส่วนคอลัมน์อื่น ๆ จะแปลงด้วยโค้ดด้านล่างนี้ โดยที่

- `'Int64'` คือตัวแปรจำนวนเต็ม (integer) ขนาด 64 บิต ที่รองรับการเก็บค่า `NaN`

**คำถาม:** ขอให้นักศึกษาอภิปรายประเด็นต่อไปนี้

1. เดิม `'StockCode'` เป็นประเภท `object` นั้นไม่ดีอย่างไร แล้วทำไมไม่แปลงเป็น `int`
2. ทำไมไม่แปลง `'CustomerID'` เป็น `int` หรือ?


```{code-cell}
:id: DOtjccWG6Tn5

data['StockCode'] = data['StockCode'].astype('string')    # ทำไมไม่เป็น .astype(int)
data['Description'] = data['Description'].astype('string')
data['CustomerID'] = data['CustomerID'].astype('Int64')   # ทำไมไม่เป็น .astype(int)
data['Country'] = data['Country'].astype('string')
```

+++ {"id": "VcvDK6Le-ES8"}

**เฉลย:**

1. เพราะ `StockCode` ไม่ใช่ตัวเลขเท่านั้น แต่มีรหัสที่เป็นตัวอักษรด้วย ดังนั้นจึงแปลงเป็น `int` ไม่ได้อยู่แล้ว ส่วนเหตุผลที่ไม่เก็บเป็น `object` ก็เช่น ใช้ String method ไม่ได้ หรือในแง่ของการใช้งาน การที่มีทั้ง `int` และ `string` ปนกัน ก็อาจสับสนเวลาใช้ เช่น จะใช้ `StockCode == 55555` กับ `StockCode == '55555'` กันแน่ เป็นต้น
2. เพราะ `CustomerID` มี `NaN` ซึ่ง ตัวแปร `int` ธรรมดาของ `Python` ไม่รองรับ

+++ {"id": "YXuVr9yEc3Fp"}

## เกร็ด: การทำซ้ำข้อมูล `DataFrame` ด้วย `.copy()`

+++ {"id": "0YqsYrrjZ9Bq"}

เนื่องจากในหัวข้อต่อ ๆ ไป จะมีการแก้ไข `DataFrame` ไปเรื่อย ๆ ดังนั้น จึงขอคัดลอกตัวแปร `data` ไว้อีกฉบับหนึ่งในชื่อ `original_data` ดังนี้

```{code-cell}
:id: cER39OX3Z8eY

original_data = data.copy()
```

+++ {"id": "OihYvXxCa4IO"}

โดยการทดลองต่าง ๆ ให้ใช้ตัวแปร `data` และในกรณีที่ต้องการโหลดข้อมูลต้นฉบับมาใหม่ ให้ใช้คำสั่ง

```
data = original_data.copy()
```

ซึ่งจะเป็นการโหลดต้นฉบับ กลับมาให้ตัวแปร `data`

+++ {"id": "DzWeAs64dt43"}

### ทำไมต้องใช้ `.copy()` ?

อย่างไรก็ตาม อาจมีคำถามว่า ทำไมจึงต้องใช้ `.copy()`  เหตุใดไม่เขียนโค้ด ดังนี้

```python
new_data = data   # ไม่มี .copy()
```
คำตอบก็คือ การเขียนแบบนี้ จะได้ตัวแปร `new_data` ที่หมายถึงข้อมูลที่เก็บใน RAM ที่เดียวกับของตัวแปร `data` แม้ชื่อจะต่างกัน (หรือพูดง่าย ๆ ว่า `new_data` เป็นชื่อเล่น ของ `data`) ดังนั้น หากมีการแก้ไข `data` หรือ `new_data` ตัวใดตัวหนึ่ง ด้วยคำสั่งของ `Pandas` บางคำสั่ง อาจทำให้ตัวแปรอีกตัวเปลี่ยนตามด้วย ซึ่งจะไม่ตรงกับจุดประสงค์ของเราที่ต้องการสำรองค่าตัวแปรไว้

เพื่อทำความเข้าใจ ขอให้นึกศึกษา พิจารณา 3 กรณี ต่อไปนี้

+++ {"id": "RpkhzfpWlvw8"}

**กรณีที่ 1** จะเห็นว่า เมื่อไม่ใช้ `.copy()` เมื่อมีการแก้ไข `new_data` กลับทำให้ `data` เปลี่ยนตาม (จำนวนแถวลดลง)

**แบบนี้ต้องระวัง!!! อาจส่งผลให้การคำนวณต่อจากนั้นผิดพลาด**

เพราะ `new_data` เป็นชื่อเล่นของ `data` ที่หมายถึงข้อมูลที่เก็บไว้ใน RAM ที่เดียวกัน

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: C9UPq3MSghfK
outputId: 7e131784-d006-46bd-fa94-852815356caa
---
data = original_data.copy()  # โหลดข้อมูลต้นฉลับ
new_data = data              # กำหนดค่าโดยไม่มี .copy()
print(f'ก่อน: data.shape={data.shape}, new_data.shape={new_data.shape}')
new_data.dropna(inplace=True)  # ใช้ inplace=True (.dropna อยู่ในหัวข้อ Q3.3)
print(f'หลัง: data.shape={data.shape}, new_data.shape={new_data.shape}')
```

+++ {"id": "R-wKjVGrl2x_"}

**กรณีที่ 2** จะเห็นว่า เมื่อใช้ `copy()` เมื่อมีการแก้ไข `new_data` ไม่ทำให้ `data` เปลี่ยนตาม

**แบบนี้ OK**

เพราะ `copy()` ทำให้ `new_data` กับ `data` เก็บข้อมูลใน RAM คนละที่

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: bd6IFPJmlDRJ
outputId: b7b5cf32-34f4-40cf-f835-46cd2f5458b9
---
data = original_data.copy()   # โหลดข้อมูลต้นฉลับ
new_data = data.copy()        # กำหนดค่าโดยมี .copy()
print(f'ก่อน: data.shape={data.shape}, new_data.shape={new_data.shape}')
new_data.dropna(inplace=True)  # ใช้ inplace=True
print(f'หลัง: data.shape={data.shape}, new_data.shape={new_data.shape}')
```

+++ {"id": "OvZZ4FSPmAmx"}

**กรณีที่ 3**  จะเห็นว่า ไม่ใช้ `copy()` เมื่อมีการแก้ไข `new_data` กลับทำให้ `data` เปลี่ยนตาม (จำนวนแถวลดลง)

**แบบนี้ก็ OK แต่จะเกิดข้อผิดพลาดภายหลังหากเผลอใช้ `inplace=True`**

สาเหตุที่แบบนี้ไม่เกิดปัญหา แม้ว่าตอนแรก `new_data` กับ `data` จะหมายถึงข้อมูลใน RAM ที่เดียวกัน แต่คำสั่ง `new_data.dropna()` ให้ค่าที่ RAM ตำแหน่งใหม่ ซึ่งเราก็ไปตั้งชื่อมันว่า `new_data`

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: CvEEc2Q2lOK3
outputId: d6ba0f66-73e3-48b3-a237-bc74d591fca7
---
data = original_data.copy()    # โหลดข้อมูลต้นฉลับ
new_data = data                # กำหนดค่าโดยไม่มี .copy()
print(f'ก่อน: data.shape={data.shape}, new_data.shape={new_data.shape}')
new_data = new_data.dropna()   # ไม่ใช้ inplace=True
print(f'หลัง: data.shape={data.shape}, new_data.shape={new_data.shape}')
```

+++ {"id": "zPw9RBimzDNv"}

## Q3 ข้อมูลที่ขาดหาย (Missing value)

ข้อมูลที่ขาดหาย ก็คือข้อมูลที่ว่างเปล่าตั้งแต่ในไฟล์ CSV หรือ Excel ซึ่งพออ่านเข้ามาใน `Pandas` จะถูกแทนที่ด้วยค่า `NaN` หรือ `<NA>` (หรือเรียกว่า null) [ดูคู่มือ](https://pandas.pydata.org/docs/user_guide/missing_data.html)

ข้อมูลขายของออนไลน์ในคาบนี้มีความยากกว่าข้อมูลการให้ทิปในคาบก่อนอยู่มาก ส่วนหนึ่งก็มาจากข้อมูลที่ไม่สมบูรณ์ การตรวจสอบข้อมูลที่ขาดหายไป ดูได้จาก `DataFrame.info()` เหมือนเช่นในคาบผ่านมา

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: jhoWvL9CzyrM
outputId: 434300a6-f782-4003-ce37-53dd7e8ee9e2
---
data.info()
```

+++ {"id": "kPbGfgwF0GOp"}

หรืออาจคำนวณเองได้จากฟังก์ชัน `DataFrame.isna()` ซึ่งจะให้ผลลัพธ์เป็น `DataFrame` ที่เก็บตัวแปร `bool` ทั้งหมด  

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 206
id: v6BZj3Pp0J2T
outputId: b4aedccc-f07a-442f-b8c8-5d00d53a76f5
---
flags = data.isna()
flags.sample(5)  # False แปลว่ามีข้อมูล แต่ถ้า True แปลว่า missing value
```

+++ {"id": "ukElK0hA0_iT"}

และเนื่องจาก `False` สามาถแปลงเป็นค่า `0` และ `True` สามารถแปลงเป็นค่า `1` ได้อัตโนมัติ ดังนั้น จึงใช้ฟังก์ชัน `DataFrame.sum()` ในการนับจำนวน missing value ได้

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: FTL7GZAW091p
outputId: bb4a62cf-a44c-473e-bda1-d05a66e1df55
---
flags.sum()
```

+++ {"id": "MYURe9ECz8V5"}

จากรายงาน จะเห็นว่าข้อมูลทั้งหมดมี 74,802 แถว แต่ `Description` มีข้อมูลขาดหายไป 237 ตำแหน่ง ส่วน `CustomerID` ขาดหายไป 19638 ตำแหน่ง

หากจะลองสุ่มตรวจดูแถวที่มี `CustomerID` เป็น `NaN` ก็สามารถทำได้ ดังนี้

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 206
id: ZgKcoGab4fg7
outputId: 3772ffae-3611-4b11-a342-c37dc81bba69
---
data[data['CustomerID'].isna()].head()
```

+++ {"id": "Uo5QJm776Xlj"}

**ลองดู:** นอกจากฟังก์ชัน `.isna()` แล้ว ยังมีอีกฟังก์ชันคือ `.notna()` ซึ่งทำงานในลักษณะกันข้าม ขอให้ทดลองด้วยตนเองว่า `.notna()` ใช้แล้วให้ผลอย่างไร

+++ {"id": "Ulnp1pbi4-L9"}

### Q3.1 ถ้าไม่อยากมองข้าม `NaN` ต้องกำหนด `dropna=False`

โดย default นั้น ฟังก์ชันบางฟังก์ชันของ `Pandas` จะมองข้ามค่า `NaN` เช่น ฟังก์ชัน

- `Series.value_counts()` (เนื้อหาคาบที่ผ่านมา)
- `Series.nunique()`  (เนื้อหาคาบที่ผ่านมา)
- `DataFrame.groupby()`  (ยังไม่ได้สอน)

ดังนั้นจึงเป็นสิ่งที่ควรระวังหากจำเป็นจำต้องสนใจค่า `NaN` ด้วย จะต้องเรียกใช้ โดยกำหนด

- `Series.value_counts(dropna=False)`
- `Series.nunique(dropna=False)`  
- `DataFrame.groupby(..., dropna=False)`

และเพื่อเป็นตัวอย่างต่อไป จะขอยกตัวอย่างเฉพาะรายการสินค้า `StockCode == '21116'` ซึ่งคือ `OWL DOORSTOP`

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 1000
id: z25CcCXv5WS5
outputId: c6a13a36-3b32-43a2-cda9-759f5469387a
---
doorstop = data[data['StockCode'] == '21116']
print(f'จำนวนแถวเท่ากับ {len(doorstop)} แถว')
doorstop
```

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: PILpKpEJCe1I
outputId: 82792fba-8c67-4aa2-d205-f8931749098d
---
doorstop['CustomerID'].value_counts()  # มองข้าม NaN
```

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: QcpD9rnEE8NN
outputId: 6cae3b93-4991-4157-a2d0-06ac4a92f4ee
---
doorstop['CustomerID'].value_counts(dropna=False)  # จะเห็นว่านัง NaN ได้ 16 ค่า
```

+++ {"id": "PQduoQJ4Trgm"}

### Q3.2 เติมข้อมูลที่ขาดหายด้วยค่าคงที่

Missing value สามารถเติมได้โดยใช้คำสั่ง `Series.fillna()` หรือ `DataFrame.fillna()`

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 423
id: _Fu_F_wRUUjb
outputId: 29cec2db-8aef-4d8e-a2ab-527c514b66c2
---
data['Description'] = data['Description'].fillna('ไม่ทราบชื่อ')
data[data['Description'] == 'ไม่ทราบชื่อ']
```

+++ {"id": "QqZmQ3KabaIm"}

### Q3.3 ไม่รู้จะเติม `NaN` ด้วยอะไร ก็ลบซะเลย

ก่อนอื่น เนื่องจาก `data` ถูกเปลี่ยนค่า `NaN` ไปในข้อ Q3.2 ดังนั้น จึงขอโหลดต้นฉบับกลับมา

```{code-cell}
:id: _NS-ed3WbZtJ

data = original_data.copy()
```

+++ {"id": "DioojZH1uEMq"}

สามารถใช้คำสั่ง `DataFrame.dropna()` ในการลบแถว ซึ่งมีพารามิเตอร์ ได้แก่

- `how='any'` หมายถึง ถ้ามี `NaN` แค่ตัวเดียวในแถวนั้น ก็ให้ลบทั้งแถว หรือ `how='all'` หมายถึง ต้องมี `NaN` ทุกคอลัมน์ จึงจะลบได้ โดย `how='any'` เป็นค่า default  
- `subset=` รายการของชื่อคอลัมน์ที่จะให้พิจารณาว่ามี `NaN` หรือไม่ โดย `how`จะพิจารณาเฉพาะคอลัมน์ที่ระบุไว้ใน `subset`
- `axis=0` หรือ `axis=1`
  - หากต้องการพิจารณา `DataFrame` เป็นรายแถว ให้กำหนด `axis=0` (default)
  - หากต้องการพิจารณา `DataFrame` เป็นรายคอลัมน์ ให้กำหนด `axis=1` (ซึ่งกรณีนี้ `how=` จะพิจารณา `NaN` ของคอลัมน์หนึ่ง ๆ)
- `inplace=True` หรือ `inplace=False` หมายถึงให้เขียนทับต้นฉบับหรือไม่  

ขอให้นักศึกษาพิจารณาเปรียบเทียบการใช้งาน จากตัวอย่างต่อไปนี้

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: 4fSnHbRWvem_
outputId: 6c3001c8-5418-426b-8288-b83350cb4725
---
print(f'จำนวนแถว {len(data)} แถว (ก่อน dropna)')
no_nan = data.dropna(how='any')
print(f'จำนวนแถวที่เหลือ {len(no_nan)} แถว (หลัง dropna ด้วย how=any)')
no_nan.isna().sum()  # แถวที่มี NaN ตัวเดียวขึ้นไป ถูกลบทั้งหมด
```

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: ZEi5IRa74oPY
outputId: 9ce281ba-d9ab-4ab1-f433-ff211cf4e431
---
print(f'จำนวนแถว {len(data)} แถว (ก่อน dropna)')
no_nan = data.dropna(how='any', subset=['Description','Quantity'])
print(f'จำนวนแถวที่เหลือ {len(no_nan)} แถว (หลัง dropna ด้วย how=any, subset=[Description, Quantity])')
no_nan.isna().sum()  # แถวที่คอลัมน์ Description และ Quantity มี NaN ตั้งแต่ 1 ตัวขึ้นไป จะถูกลบทั้งหมด
```

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: Gm4v8yKlzzsr
outputId: f0a176f1-f5ca-4a92-a1da-be29321c8cea
---
print(f'จำนวนคอลัมน์ {data.shape[1]} คอลัมน์ (ก่อน dropna)')
no_nan = data.dropna(how='any', axis=1)
print(f'จำนวนคอลัมน์ที่เหลือ {no_nan.shape[1]} คอลัมน์ (หลัง dropna ด้วย how=any)')
no_nan.isna().sum()  # คอลัมน์ที่มี NaN ตัวเดียวขึ้นไป ถูกลบทั้งหมด (CustomerID กับ Description ถูกลบไป)
```

+++ {"id": "MvaU8AIc4f3C"}

## Q4 Groupby and Aggregation

หากต้องการแบ่งส่วนของตารางเป็นกลุ่มย่อย ๆ ตามค่าของคอลัมน์ ๆ หนึ่ง (หรืออาจหลายคอลัมน์) สามารถทำได้ง่ายโดยใช้ฟังก์ชัน `DataFrame.groupby()` [ดูคู่มือ](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html) และสามารถคำนวณค่าสถิติภาพรวมของแต่ละกลุ่มย่อย ด้วยการทำ aggregration (`.agg()`)

ยกตัวอย่างเช่น จากข้อมูล `data` ที่มี หากต้องการแบ่งกลุ่มย่อยตามค่าของคอลัมน์ `InvoiceNo` จะทำได้ ดังนี้

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: GJsAmBFxLjRG
outputId: 59d31df7-7bac-4932-878b-130ae0161217
---
inv_group = data.groupby('InvoiceNo', dropna=False)
inv_group
```

+++ {"id": "xEPkQsNeXnrk"}

ตัวแปร `inv_group` ที่ได้เป็นชนิดข้อมูล `DataFrameGroupBy` ของ `Pandas`

การนำกลุ่มที่แบ่งขึ้นไปใช้ประโยชนในเบื้องต้น ได้แก่

+++ {"id": "1v6cgJDqRwVe"}

### Q4.1 จะเข้าถึงกลุ่มย่อยได้อย่างไร

คำตอบคือ การเข้าได้โดยใช้คำสั่งดังนี้
```python
inv_group.get_group('ค่า InvoiceNo ที่ต้องการ')
```

เช่น จะเข้าถึงกลุ่มที่ `InvoiceNo` มีค่า `'558888'`

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 423
id: RPtN6q5PSDZ_
outputId: 0731d489-4919-4b50-9011-63075b841779
---
inv_group.get_group('558888')
```

+++ {"id": "5juD9Yl4SlHS"}

ซึ่งจะพบว่าตารางมี 87 แถว และคอลัมน์ `InvoiceNo` มีค่า `'558888'` เหมือนกันหมด

+++ {"id": "Kd8RPeQlUKLt"}

### Q4.2 การทำข้อมูลภาพรวมจากกลุ่มย่อย

การยุบคอลัมน์ในกลุ่มย่อยแต่ละกลุ่มให้เหลือเพียงค่าเดียว เช่น การหาค่าเฉลี่ย ค่าสูงสุด หรือจำนวนแถวของคอลัมน์ เป็นต้น เรียกว่าการทำ aggregration ซึ่งสามารถทำโดยใช้คำสั่ง

`group.sum()`, `group.min()` , `group.max()`, .... ฯลฯ หรือ `group.agg(['sum','min','max', ...])`

ซึ่งเป็นคำสั่งเดียวกับที่ได้ศึกษาในคาบที่ผ่านมา  (แต่เป็นคาบนั้นเป็นการหาค่าสถิติของทั้งตาราง)
ยกตัวอย่างเช่น

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 454
id: TZ5Vo7rtVePk
outputId: 3bab22fc-c8b1-4002-8246-c6560efc1289
---
inv_group.max(numeric_only=True)  # กำหนด numeric_only=True เพื่อที่จะคำนวณ sum เฉพาะคอลัมน์ที่เป็นตัวเลข
```

+++ {"id": "uP0yhlfAfGw-"}

จะเห็นว่า ผลลัพธ์ของ aggregration ด้วย `.max()` นั้น จะได้ `DataFrame` (หรืออาจเป็น `Series` กรณีข้อมูลมีคอลัมน์เดียว) ที่แต่ละแถวแสดงค่าสูงสุดของแต่ละกลุ่ม

ทั้งนี้ สามารถเลือกคอลัมน์ที่ต้องการทำ aggregration ได้เหมือนกับการเข้าถึงคอลัมน์ของ `DataFrame` ดังเช่น

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 454
id: DupgbTI5eYmv
outputId: ec6aa626-1337-4be3-ef2a-f5a3ad633ed4
---
inv_group[['UnitPrice','Quantity']].max()  # สามารถเลือกเฉพาะคอลัมน์ได้
```

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 486
id: iYQBQ7hDhc7p
outputId: 4971e634-670e-4455-aa79-d2e15be5c51d
---
inv_group[['UnitPrice','Quantity']].agg(['max','min'])
```

+++ {"id": "VZOqTk_qO1iW"}



### Q4.3 จะทราบได้อย่างไรว่า `group` ที่ได้มีกี่กลุ่ม อะไรบ้าง

คำตอบคือ สามารถนับจำนวนกลุ่มโดยใช้ `.ngroups` และสามารถเข้าถึงชื่อกลุ่มทั้งหมดได้จาก `.groups.keys()` ดังตัวอย่างต่อไปนี้

**1) นับจำนวนกลุ่ม**

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: d9VG0JtMKjFA
outputId: bc048eda-7631-466f-9117-9ef378df1e2d
---
inv_group.ngroups
```

+++ {"id": "TjRXWLHIQsBD"}

จะเห็นว่ามีทั้งหมด 3664 กลุ่ม ซึ่งตรวจสอบด้วยคำสั่ง

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: IeDBB7jSQyDI
outputId: d5a206ee-719d-4c7f-9f3f-ca592106dd7f
---
data['InvoiceNo'].nunique(dropna=False)
```

+++ {"id": "wRYWZHZqRTBM"}

**2) รายชื่อกลุ่มทั้งหมดที่เป็นไปได้**

```
inv_group.groups.keys()   # ให้นักศึกษาลองใช้ดู
```

+++ {"id": "rvbYMLq6GwdD"}

## Q5 เกี่ยวกับข้อมูลวันที่ (`datetime`)

+++ {"id": "3KrojF9Gy4c9"}

### Q5.1 การแปลง `string` เป็น `datetime`

สมมติว่ามี `string` ที่เก็บค่าวันที่ ดังนี้

- `start_date = '20/12/2023'`
- `end_date = '25/12/2023'`

เราคาดหวังว่า เมื่อเปรียบเทียบ `start_date < end_date` แล้วจะต้องได้ค่า `True` แต่ทว่าการกระทำเช่นนี้ไม่สามารถทำได้โดยง่ายระหว่างตัวแปรประเภท `string`

ด้วยเหตุนี้ จึงเกิดตัวแปรประเภท `datetime` ขึ้น ซึ่งวิธีสร้างตัวแปร `datetime` วิธีหนึ่ง ก็คือการแปลงจาก `string` ให้เป็น `datetime` โดยใช้คำสั่งต่อไปนี้

```python
pd.to_datetime(สตริงที่ต้องการแปลง, format=รูปแบบของวันเวลา)
```



ยกตัวอย่างเช่น

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: CsP6Pj5qBBcw
outputId: a01d078a-ed09-40c4-de75-de50169a774f
---
birth_time = '19-Mar-98 15:34:56'  # = 19 March 1998 15:34:56
birth_time = pd.to_datetime(birth_time, format='%d-%b-%y %H:%M:%S')
birth_time
```

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: ksNu1GUo60ao
outputId: d89f8f64-2b1e-47f7-df7b-9dc1fc2b7c92
---
start_date = '20/12/2023'
end_date = 'December 25, 2023'

start_date = pd.to_datetime(start_date, format='%d/%m/%Y')
end_date = pd.to_datetime(end_date, format='%B %d, %Y')
print(start_date)
print(end_date)
print(start_date < end_date) # เปรียบเทียบวันเวลาได้
print(start_date > end_date) # เปรียบเทียบวันเวลาได้
```

+++ {"id": "gVfHiwUnAEle"}

ซึ่งรูปแบบของวันเวลา ดูได้ตาม[คู่มือ](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior)ฟังก์ชัน `strftime()` ของภาษา `Python` ที่ `Pandas` เรียกใช้งาน

สำหรับรูปแบบของวันเวลาที่แสดงในตัวอย่าง เครื่องหมาย `%` แต่ละตัวมีความหมาย ดังตาราง

| คำสั่ง | ความหมาย | ตัวอย่าง |
|:--:|:--|:--|
| `%d` | วันที่ 2 หลัก  | `01, 02, …, 31` |
| `%m` | เลขเดือน 2 หลัก |  `01, 02, …, 12` |
| `%b` | ชื่อเดือนย่อ | `Jan, Feb, …, Dec` |
| `%B` | ชื่อเดือนเต็ม | `January, February, …, December` |
| `%y` | เลขปี 2 หลักท้าย (ละเลขศตวรรษ) | `00, 01, …, 99` |
| `%Y` | เลขปี 4 หลัก | `0001, 0002, …, 9999` |
| `%H`| ชั่วโมง | `00, 01, …, 23` |
| `%M`| นาที | `00, 01, …, 59` |
| `%S` |วินาที |`00, 01, …, 59` |


+++ {"id": "rcmBNpE2G67n"}

หากตัวแปรเป็นประเภท `datetime` แล้ว ก็จะสามารถเข้าถึงค่าวัน เดือน ปี ชั่วโมง นาที วินาที สัปดาห์ที่ ได้ ดังตัวอย่างนี้

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: MR6clRNUHWke
outputId: dc61d93b-4102-44ce-ff06-62a924785814
---
print(birth_time)
print('Year =', birth_time.year)
print('Month =', birth_time.month)
print('Day =', birth_time.day)
print('Week =', birth_time.week)
print('Hour =', birth_time.hour)
print('Minute =', birth_time.minute)
print('Second =', birth_time.second)
```

+++ {"id": "pNWsk7mcHDpl"}

### Q5.2 การคำนวณส่วนต่างของเวลา

หากมีตัวแปร `datetime` 2 ตัว จะสามารถคำนวณความแตกต่างระหว่างวันเวลาได้ ดังเช่น

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: oidwolVDA_6_
outputId: ef31bce5-e449-4cf3-cef7-bc233feed5e4
---
print(f'start = {start_date}')
print(f'end   = {end_date}')
difference = end_date - start_date
print(difference)
```

+++ {"id": "LRn6c02zGTEh"}

โดยผลลัพธ์ที่ได้ในตัวแปร `difference` จะได้ตัวแปรประเภท `timedelta`

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: AlrEBdJ-Pexq
outputId: 30b54877-1234-470d-fcb5-b016e3078d7a
---
print(type(difference))
```

+++ {"id": "3580XLS5PiX-"}

ซึ่งส่วนต่าง 5 วัน ที่คำนวณได้ สามารถถึงค่าจำนวนวันออกมาได้ด้วย `.days`

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: nzweyJ1SO7c9
outputId: b70d7380-da0f-4e50-8beb-99ef7b8435f3
---
difference.days
```

+++ {"id": "QT2GgLsKHNI0"}

### Q5.3 `datetime` ใน `Series/DataFrame`

`Series` หรือ `DataFrame` สามารถแปลงให้เป็น `datetime` ได้ โดยใช้ฟังก์ชัน `pd.to_datetime()` เช่นกัน แต่สำหรับข้อมูลร้านขายของออนไลน์ในคาบนี้ คอลัมน์ `InvoiceDate` ถูกแปลงเป็นประเภท `datetime` โดยอัตโนมัติอยู่แล้ว ดังนั้นจึงไม่ต้องทำอะไรเพิ่มเติม

ดังนั้นในส่วนนี้ จะยกตัวอย่างของการดึงค่าจากตัวแปร `datetime` ที่เป็นเลขสัปดาห์ที่, เลขเดือน, และเลขชั่วโมง ไปสร้างเป็น 3 คอลัมน์ใหม่

+++ {"id": "IVkMKb3TYxdm"}

#### เพิ่มคอลัมน์เลขเดือน

```{code-cell}
:id: DbtfGUbXY_k_

data['MonthNo'] = data['InvoiceDate'].dt.month
```

+++ {"id": "VAXgO7wuY8MZ"}

#### เพิ่มคอลัมน์เลขสัปดาห์

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: XN_2ASFzY3IF
outputId: 44621d50-359e-4e90-d660-28dd41f51814
---
data['WeekNo'] = data['InvoiceDate'].dt.isocalendar().week  # ใช้ Series.dt.week ไม่ได้
```

+++ {"id": "IBbtjMmsZBjk"}

#### เพิ่มคอลัมน์สถานะว่าคำสั่งซื้อมาก่อน 12.00 น. หรือไม่

```{code-cell}
:id: YF2Jx8H_ZSkc

data['BeforeNoon'] = (data['InvoiceDate'].dt.hour <= 12)
```

+++ {"id": "lIdvpdkrZZUY"}

#### เพิ่มคอลัมน์สถานะว่าคำสั่งซื้อมาก่อนวันคริสต์มาสปี 2011 กี่วัน

```{code-cell}
:id: Q975MqQ5Js_o

xmas = '2011-12-25'
data['DaysToXmas'] = (pd.to_datetime(xmas) - data['InvoiceDate']).dt.days  # เอาเฉพาะจำนวนวัน
```

+++ {"id": "YLqBXr0OUFeZ"}

#### ตอบคำถามว่า `InvoiceDate` แรกสุดและล่าสุดในคือวันและเวลาใด

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: l1ThU1ivZtqx
outputId: c7e35590-808a-4a2d-a38c-7032a1b807c0
---
data['InvoiceDate'].agg(['min','max'])
```

+++ {"id": "lAy63OTbFf4g"}

## Q6 การรายงานข้อมูลเป็นรายลูกค้า

จากข้อมูลที่มี ในช่วง 2 เดือน จะตอบคำถามต่อไปนี้

1. ลูกค้าแต่ละคน มีจำนวน Invoice เกิดขึ้นกี่ Invoice และเกี่ยวข้องกับสินค้าทั้งหมดกี่ชนิด (`StockCode`)
2. ลูกค้าแต่ละคนเข้ามาแรกสุดและล่าสุดเมื่อใด (จากข้อมูลทั้งหมดที่มี)
3. ยอดซื้อรวมของลูกค้าแต่ละคน

ซึ่งทำได้ 2 วิธี




+++ {"id": "5xSxhuihrArC"}

### **วิธีที่ 1** ทำ 1,2,และ 3 แล้วค่อยนำมารวมกัน

+++ {"id": "gIqto26mi2jD"}

#### 1. ลูกค้าแต่ละคน มีจำนวน Invoice เกิดขึ้นกี่ Invoice และเกี่ยวข้องกับสินค้าทั้งหมดกี่ชนิด (`StockCode`)

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: 1UW0Ahbfgrbn
outputId: 2c66fed6-b552-4bd0-fedf-7f943f2c2bce
---
customer_invoiceno = data.groupby('CustomerID')[['InvoiceNo','StockCode']].nunique()
print(customer_invoiceno.shape)
```

+++ {"id": "8Pr-y6J6JsJr"}

#### 2. ลูกค้าแต่ละคนเข้ามาแรกสุดและล่าสุดเมื่อใด (จากข้อมูลทั้งหมดที่มี)

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: aQBivlfoasb4
outputId: 6c51f7d1-285a-4160-f367-01823ed5c9d4
---
customer_duration = data.groupby('CustomerID')['InvoiceDate'].agg(['min','max'])
print(customer_duration.shape)
```

+++ {"id": "VCnn5S17pIL_"}

#### 3. ยอดซื้อรวมของลูกค้าแต่ละคน

ก่อนอื่น ต้องคำนวณยอดรวมของแต่ละรายการก่อน ด้วยการนำราคาต่อหน่วยมาคูณกับจำนวนชิ้นที่ซื้อ

```{code-cell}
:id: _KV6Dy6BpCsG

data['Total'] = data['UnitPrice']*data['Quantity']
customer_total_spend = data.groupby('CustomerID')['Total'].agg(['sum'])
```

+++ {"id": "foaUZ8BbjufT"}

#### การนำคอลัมน์มาต่อกัน

จากต้นคาบ นักศึกษาได้ใช้ `pd.concat()` ไปแล้ว แต่เป็นการนำสองตารางมาต่อกันในแนวดิ่ง

สำหรับในหัวข้อนี้ เราต้องการนำตารางมาต่อกันในแนวราบ กล่าวคือ แต่ละแถวที่มี `CustomerID` ตรงกัน จะถูกนำมาต่อกัน ซึ่งสามารถทำได้ด้วยคำสั่ง `pd.concat(..., axis=1)` ที่เพิ่มพารามิเตอร์ `axis=1` เข้ามา

อนึ่ง ใน `Pandas` นั้น มีการนิยามแกน (axis) เป็นค่า ดังนี้
- `axis=0` หมายถึงแกนนอน (กระทำกับคอลัมน์ที่ชื่อเหมือนกัน) (มักใช้เป็นค่า **default** ในหลายฟังก์ชัน)
- `axis=1` หมายถึงแกนตั้ง (กระทำกับแถวที่ index เหมือนกัน) (โดยปกติมักจะต้องระบุเอง)


```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 454
id: YZaYUfLKjbe2
outputId: ab234380-c421-49e8-df24-e4aa2287a8e8
---
pd.concat( (customer_invoiceno, customer_total_spend, customer_duration), axis=1)
```

+++ {"id": "U551exJqp52-"}

### **วิธีที่ 2** การทำ Aggregration โดยการระบุฟังก์ชันจำเพาะกับแต่ละคอลัมน์

วิธีการนี้ ทำได้โดยการส่ง Dictionary ให้กับ `.agg` ดังนี้

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 486
id: ELevmUpuqA-a
outputId: b771c14a-5df2-41fa-9a30-5c5450c0e98e
---
data.groupby('CustomerID').agg(
    {'InvoiceNo':['nunique'],
     'StockCode':['nunique'],
     'Total':['sum'],
     'InvoiceDate':['min','max'],
     }
)
```

+++ {"id": "oqgJGrVNydcY"}

**ลองทำ**

ก่อนจบจากส่วนนี้ และเข้าสู่เนื้อหาของการวาดกราฟ ขอให้นักศึกษาศึกษา การใช้งานฟังก์ชัน `to_excel()` ตามลิงค์นี้

https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_excel.html

เพื่อบันทึกตารางผลลัพธ์ที่ได้จากการทำ aggregation ลงไฟล์ Excel จากนั้นลองดาวน์โหลดไฟล์ที่ได้ ไปเปิดในโปรแกรม Excel ในเครื่องคอมพิวเตอร์ของนักศึกษา

+++ {"id": "sECFmTLJqJCE"}

## การวาดกราฟ

ในหัวข้อนี้ จะมุ่งเน้นที่การวาดกราฟแบบต่าง ๆ  แต่เนื่องจากข้อมูลที่มีจำเป็นต้องทำการ clean ก่อน ซึ่งจะทำดังนี้

### Data cleansing

การทำความสะอาดข้อมูล จะทำความสะอาดอะไรบ้าง จำเป็นจะต้องทราบก่อนว่าจะวิเคราะห์ไปเพื่ออะไร สมมติว่าสนใจวิเคราะห์เกี่ยวกับพฤติกรรมของลูกค้า ดังนั้น จึงขอทำความสะอาดข้อมูลดังนี้

1. เนื่องจากสนใจเฉพาะแถวที่เป็นคำสั่งซื้อของลูกค้า ดังนั้นจึงจำเป็นต้องมี `CustomerID` จึงลบแถวที่มี `CustomerID` เป็น `NaN` ออกไป
2. ลบ `InvoiceNo` ที่ขึ้นต้นด้วย `C` และ `A` เพราะคำสั่งซื้อที่ถูกยกเลิกถูกลง `UnitPrice` เป็น `0`
3. ไม่สนใจ `UnitPrice` เท่าับ `0` เพราะอาจเป็นของแจกฟรี (สมมติฐาน)

```{code-cell}
:id: Ii3PO-sCa6ss

df = data.dropna(subset=['CustomerID'])  # ข้อ 1
df = df[~(df['InvoiceNo'].str.startswith('A') | df['InvoiceNo'].str.startswith('C'))]  # ข้อ 2
df = df[df['UnitPrice'] > 0]  # ข้อ 3
```

+++ {"id": "bvQLXcySM3ut"}

### ลูกค้ามาจากไหนบ้าง

ก่อนอื่น นักศึกษาลองหาสิว่า จากข้อมูลในตัวแปร `df`
- มีลูกค้าทั้งหมดกี่ราย
- มีประเทศที่เป็นไปได้ทั้งหมด กี่ประเทศ

+++ {"id": "Pegc2WMxnpWR"}

#### การแจกแจงจำนวนลูกค้าตามรายประเทศ

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 542
id: MpaUUfGMn8IW
outputId: 9e05804e-466b-4dbc-e2ff-181d2b1c0c50
---
import plotly.express as px
per_customer = df.drop_duplicates(subset=['Country','CustomerID'])
n_customers = per_customer.groupby('Country')['CustomerID'].count()  # ได้ Series
px.bar(n_customers, text_auto=True, title='การแจกแจงจำนวนลูกค้าตามรายประเทศ แบบที่ 1')
```

+++ {"id": "ycK7-_asOHwU"}

แต่เนื่องจาก United Kingdom มีมากเกินไป ทำให้อ่านกราฟได้ยาก จึงขอตัดออกจากกราฟเลย ด้วยคำสั่ง `Series.drop()` ดังนี้

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 542
id: y5EwjkBupM0J
outputId: 6835fed8-a34d-4c02-b4f3-f03fd3c4db56
---
n_customers = per_customer.groupby('Country')['CustomerID'].count().drop('United Kingdom')
px.bar(n_customers, text_auto=True, title='การแจกแจงจำนวนลูกค้าตามรายประเทศ แบบที่ 2 (exclude UK)')
```

+++ {"id": "p6pK5X6qOSfW"}

หรืออีกทางเลือกหนึ่งคือ ใช้แกนตั้งให้เป็น log scale โดยใช้พารามิเตอร์ `log_y=True`

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 542
id: NZn7z3OJN-xc
outputId: 4a8afa54-1627-4d1d-83e4-84c2fc2026d2
---
n_customers = per_customer.groupby('Country')['CustomerID'].count()
px.bar(n_customers, text_auto=True, log_y=True, title='การแจกแจงจำนวนลูกค้าตามรายประเทศ แบบที่ 3 (log-scale)')
```

+++ {"id": "QgJaWkMZn2XU"}

หรือจะลองใช้ Pie chart ([คู่มือ](https://plotly.com/python/pie-charts/)) แทน Bar chart

รูปแบบการใช้คำสั่งสร้าง Pie chart คือ

```python
px.pie(ข้อมูลที่เป็นDataFrame, values=ชื่อคอลัมน์ที่เก็บตัวเลข, names=ชื่อกำกับตัวเลข)
```


```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 206
id: F4vwwBEGPTZo
outputId: 4d151671-232c-4d83-e632-e9f9a92fc54c
---
n_customers = ( per_customer.groupby('Country')['CustomerID']
                    .nunique()      # ได้ Series ที่มี Country เป็น index โดยที่ Series ถูกตั้งชื่อว่า CustomerID
                    .rename('No of customers')  # ไม่ต้องการให้ Series ชื่อ CustomerID จึงแก้ชื่อเป็น No of customers
                    .drop('United Kingdom')  # เอาค่าของ index='United Kingdom' ออกจาก Series
                    .reset_index()    # ทำให้ Series กลายเป็น DataFrame  ค่าของ Series จะกลายมาเป็นคอลัมน์ชื่อ No of customers
)
n_customers.head()
```

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 542
id: MqZmyrW7SdXu
outputId: 9243e4e7-61eb-46cc-9820-97de17ce088e
---
px.pie(n_customers, values='No of customers', names='Country',  title='การแจกแจงสัดส่วนลูกค้าตามรายประเทศ แบบที่ 4 (exclude UK)')
```

+++ {"id": "SKd-tzNUTWZQ"}

### คำสั่งซื้อจากแต่ละประเทศ เกิดขึ้นก่อนเที่ยงหรือหลังเที่ยง

ตัวอย่างนี้เป็นเพียงตัวอย่างการวาดกราฟเท่านั้น แต่ข้อเท็จจริงที่นำไปวาดกราฟอาจไม่ถูกต้อง เนื่องจากไม่ทราบว่า `InvoiceDate` คือเวลาใน Time zone ไหน จึงขอตั้งสมมติฐานว่าเป็นเวลาของ UK เนื่องจากบริษัทจดทะเบียนที่ UK และลูกค้าส่วนใหญ่มาจาก UK

```{code-cell}
:id: 2i8HkUv5EH6x

df2 = df.drop_duplicates(subset=['InvoiceNo','Country','BeforeNoon'])
df2 = df2[['InvoiceNo','Country','BeforeNoon']].sort_values(by='Country')
```

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 542
id: Zf9P4tGE2BDJ
outputId: ffe92b5a-be0e-49ad-9500-31987e028684
---
fig = px.histogram(df2, x='Country',
                   color='BeforeNoon',
                   barmode='group',
                   text_auto=True,
                   log_y=True)
fig.show()
```

+++ {"id": "BO2lsbtb1FV1"}

หากสงสัยว่ากราฟที่วาด ผิดหรือไม่ ก็ตรวจสอบได้จากคำสั่งของ `Pandas` อีกทาง

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: eoN4PBDK1PZQ
outputId: 2e04dbde-682b-45fd-c7a5-e7db9cf94ed3
---
df2.groupby('Country')['BeforeNoon'].value_counts()
```

+++ {"id": "6lTlBsv9iPyK"}

### ปริมาณคำสั่งซื้อต่อวันเป็นอย่างไรบ้าง

ขอให้นักศึกษาลองคิดดูว่า การจะคำนวณปริมาณคำสั่งซื้อในแต่ละวัน จะทำได้อย่างไร นักศึกษาอาจดึงเฉพาะวันที่ออกจาก `InvoiceDate` (เพราะไม่อยากได้ค่าเวลา) ไปสร้างเป็นคอลัมน์ใหม่แล้ว ซึ่งหากนำวันที่มาจัดกลุ่มด้วย `groupby` ก็จะได้กลุ่มย่อยของ `InvoiceNo` เป็นรายวัน ซึ่งสามารถนับจำนวน `InvoiceNo` ที่ไม่ซ้ำกันในหนึ่งวัน ได้ด้วย `nunique()` ดังนี้


```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 542
id: zK38zxiD3081
outputId: 4315a97e-a0b1-4516-ae59-820b8cc06a6d
---
df['InvoiceDateOnly'] = df['InvoiceDate'].dt.date   # dt.date จะใด้ datetime แต่ dt.day จะได้เลขวันที่
invoice_by_day = df.groupby('InvoiceDateOnly')['InvoiceNo'].nunique()
px.line(invoice_by_day, markers=True, title='ปริมาณคำสั่งซื้อในแต่ละวัน (แบบที่ 1 ใช้ groupby)')
```

+++ {"id": "2DhiN0W85ef8"}

อย่างไรก็ตาม กราฟที่ได้จะข้ามบางวันไป ซึ่งดูจากกราฟอาจจะดูไม่ค่อยออก ดังนั้น ในหลายกรณี จึงจำเป็นที่จะต้องเติมวันที่ที่ขาดหายไปเข้าไปด้วย ดังนั้นจึงเป็นที่มาของการวาดกราฟแบบที่ 2 ที่ใช้คำสั่ง `set_index()` ตามด้วย `resample()`

#### คำสั่ง `set_index()`

เป็นคำสั่งที่ใช้กำหนดให้คอลัมน์ที่ต้องการ กลายเป็น `index` ของ `DataFrame`

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 448
id: t195E4g67pI7
outputId: 799a8f25-45e8-4fdc-eb18-a7b3032b7823
---
df2 = df.set_index('InvoiceDate')
df2.head()
```

+++ {"id": "Eg5LajpE8Fap"}

จะเห็นว่า ตอนนี้ `InvoiceDate` ถูกเปลี่ยนให้เป็น index โดยที่คอลัมน์ `InvoiceDate` เดิม และ index เดิมก็หายไปด้วย ทั้งนี้มีข้อสังเกตุคือ การที่ `InvoiceDate` มีค่าซ้ำกันได้  ทำให้ index ที่ได้มีค่าไม่เป็นเอกลักษณ์เฉพาะแถว

เมื่อได้ index ที่เป็นวันเวลา โดยที่วันเวลาถูกเรียงลำดับจากน้อยไปมากไว้ก่อนแล้ว (หากยังไม่เรียง ก็ให้ใช้ `DataFrame.sort_index()` ก่อน) จะสามารถใช้คำสั่ง `resample() ได้ ` ([คู่มือ](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#resampling)  ซึ่ง `resample()` จะทำงานคล้าย `groupby` และยังสามารถเติมวันเวลาที่ขาดหายเข้าไปด้วย  

สำหรับในตัวอย่างต่อไปนี้ `.resample('D')` จะเป็นการไล่วันเวลาในระดับวันที่

`2011-07-01`, `2011-07-02`, `2011-07-03`, ...

ซึ่งสามารถเป็นการไล่เวลาในระดับชั่วโมง, สัปดาห์, เดือน เป็นต้น ซึ่งสามารถดูเพิ่มเติมได้จากคู่มือ

หลังจาก `resample('D')`  แล้ว จึงทำการเลือกเฉพาะคอลัมน์ `InvoiceNo` และ aggregrate ข้อมูลในแต่ละวัน ด้วยคำสั่ง `nunique()` เพื่อนับจำนวน `InvoiceNo` ที่ไม่ซ้ำกันในวันใด ๆ

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: 9MCFNWa_Dbun
outputId: c44233e3-e002-4ef0-859d-ff039ed5d6fa
---
df3 = df2.resample("D")['InvoiceNo'].nunique()
df3
```

+++ {"id": "mj5MwjD5DL9P"}

จากคำอธิบายข้างต้น สามารถนำมาสรุปเขียนเป็นคำสั่งในคราวเดียว และวาดกราฟเส้น ได้ ดังนี้

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 542
id: QjI9CJRK_s23
outputId: 06966c34-efd0-4197-b322-fbcab238feeb
---
invoice_by_day = (df.set_index('InvoiceDate')
                      .resample("D")["InvoiceNo"]
                      .nunique()
)
px.line(invoice_by_day, markers=True, title='ปริมาณคำสั่งซื้อในแต่ละวัน (แบบที่ 2 ใช้ resample)')
```

+++ {"id": "XUxQcGCt9zgq"}

จากกราฟ จะเห็นวันที่จำนวน Invoice เป็น 0 มันคือวันอะไร?

**จบเนื้อหา**

นักศึกษาลองสรุปซิว่า วันนี้นักศึกษาได้เรียนรู้คำสั่งอะไรบ้าง
