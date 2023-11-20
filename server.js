const express = require('express');
const multer = require('multer');
const path = require('path');

const app = express();
const port = 8000;

// 이미지 업로드를 위한 설정
const storage = multer.diskStorage({
  destination: './uploads/',
  filename: function (req, file, cb) {
    cb(null, file.originalname);
  }
});

const upload = multer({ storage: storage });

// 정적 파일 제공 (이미지 업로드 후 저장된 이미지를 보기 위해)
app.use('/uploads', express.static('uploads'));

// 루트 경로에 대한 GET 요청 처리
app.get('/', (req, res) => {
  res.send('Hello, this is the Bedbug Server!');
});

// 이미지 업로드를 처리할 엔드포인트
app.post('/upload', upload.single('image'), (req, res) => {
  if (!req.file) {
    return res.status(400).send('No file uploaded.');
  }

  const imageUrl = `http://localhost:${port}/uploads/${req.file.filename}`;
  res.status(200).send(`File uploaded successfully. Image URL: ${imageUrl}`);
});

// 서버 실행
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
