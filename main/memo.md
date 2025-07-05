tripmate
├── Dockerfile
├── .dockerignore
├── package.json
├── package-lock.json
├── tsconfig.json
├── public
│   ├── index.html
│   ├── image1.jpg
│   ├── image2.jpg
│   ├── image3.jpg
│   ├── image4.jpg
│   ├── image5.jpg
│   └── image6.jpg
└── src
    ├── App.tsx
    ├── App.css
    ├── index.tsx
    ├── index.css
    ├── react-app-env.d.ts
    ├── components
    │   ├── Header.tsx
    │   ├── Header.css
    │   ├── Footer.tsx
    │   └── Footer.css
    └── pages
        ├── MainPage.tsx
        ├── MainPage.css
        ├── LoginPage.tsx
        ├── LoginPage.css
        ├── SignUpPage.tsx
        ├── SignUpPage.css
        ├── SupportPage.tsx
        ├── SupportPage.css
        ├── Select.tsx        <-- 新規追加
        └── Select.css        <-- 新規追加


PS C:\develop\GinMate\main\tripmate>

docker build -t tripmate:latest .
docker run -p 3200:3200 tripmate:latest