import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './MainPage.css';

function MainPage() {
  const navigate = useNavigate();
  const images = [
    '/image1.jpg',
    '/image2.jpg',
    '/image3.jpg',
    '/image4.jpg',
    '/image5.jpg',
    '/image6.jpg',
  ];

  // スライドショー管理
  const [currentIndex, setCurrentIndex] = useState(0);
  const [prevIndex, setPrevIndex] = useState<number | null>(null);

  // モーダル表示／非表示
  const [showModal, setShowModal] = useState(false);
  const [closingModal, setClosingModal] = useState(false); // 下に閉じるアニメ用

  // 入力フォーム
  const [startDate, setStartDate] = useState('');
  const [startTime, setStartTime] = useState('');     // 出発時刻
  const [endDate, setEndDate] = useState('');
  const [endTime, setEndTime] = useState('');         // 到着時刻
  const [departure, setDeparture] = useState('');
  const [destination, setDestination] = useState('');
  const [genre, setGenre] = useState('人気');
  const [peopleCount, setPeopleCount] = useState('');
  const [budget, setBudget] = useState('');

  // 都道府県プルダウンデータ
  const prefectures = [
    {
      label: '北海道・東北',
      options: ['北海道','青森県','岩手県','宮城県','秋田県','山形県','福島県']
    },
    {
      label: '関東',
      options: ['茨城県','栃木県','群馬県','埼玉県','千葉県','東京都','神奈川県']
    },
    {
      label: '中部',
      options: ['新潟県','富山県','石川県','福井県','山梨県','長野県','岐阜県','静岡県','愛知県']
    },
    {
      label: '近畿',
      options: ['三重県','滋賀県','京都府','大阪府','兵庫県','奈良県','和歌山県']
    },
    {
      label: '中国',
      options: ['鳥取県','島根県','岡山県','広島県','山口県']
    },
    {
      label: '四国',
      options: ['徳島県','香川県','愛媛県','高知県']
    },
    {
      label: '九州・沖縄',
      options: ['福岡県','佐賀県','長崎県','熊本県','大分県','宮崎県','鹿児島県','沖縄県']
    }
  ];

  // ローディング表示 (実行ボタン後)
  const [isLoading, setIsLoading] = useState(false);

  // スライドショー (5秒ごとに切り替え)
  useEffect(() => {
    const interval = setInterval(() => {
      setPrevIndex(currentIndex);
      setCurrentIndex((prev) => (prev === images.length - 1 ? 0 : prev + 1));
    }, 5000);

    return () => clearInterval(interval);
  }, [currentIndex, images.length]);

  // 「プラン作成」ボタン => モーダル表示
  const handleOpenModal = () => {
    setShowModal(true);
    setClosingModal(false);
  };

  // 「キャンセル」ボタン => 下スライド => 非表示
  const handleCloseModal = () => {
    setClosingModal(true);
    setTimeout(() => {
      setShowModal(false);
      setClosingModal(false);
    }, 500);
  };

  // 「実行」ボタン => 4秒ロード => Reflexアプリケーションのマップ機能
  const handleExecute = () => {
    setShowModal(false);
    setIsLoading(true);

    setTimeout(() => {
      // Reflexアプリケーションのマップ機能に遷移
      const isProduction = process.env.NODE_ENV === 'production';
      const mapUrl = isProduction ? '/api' : 'http://localhost:3001';
      window.open(mapUrl, '_blank');
      setIsLoading(false);
    }, 4000);
  };

  // 「プラン確認」ボタン => http://localhost:3000
  const handleCheck = () => {
    window.location.href = 'http://localhost:3000';
  };

  return (
    <main className="main-container">
      <div className="slideshow-wrapper">
        <div
          className="slideshow-image fade-in"
          key={currentIndex}
          style={{ backgroundImage: `url(${images[currentIndex]})` }}
        />
        {prevIndex !== null && (
          <div
            className="slideshow-image fade-out"
            key={prevIndex}
            style={{ backgroundImage: `url(${images[prevIndex]})` }}
          />
        )}
      </div>

      {/* メインコンテンツ */}
      <div className="main-content">
        <div className="main-content-box">
          {/* タイトル変更 */}
          <h1 className="main-title">旅行プラン AI提案サービス</h1>

          <div className="main-buttons">
            {/* 「計画」→「プラン作成」 */}
            <button className="plan-button" onClick={handleOpenModal}>
              プラン作成
            </button>
            {/* 「確認」→「プラン確認」 */}
            <button className="check-button" onClick={handleCheck}>
              プラン確認
            </button>
          </div>
        </div>
      </div>

      {/* モーダル */}
      {showModal && (
        <div className="modal-overlay">
          <div className={`modal-content ${closingModal ? 'slide-down' : 'slide-up'}`}>
            <h2 className="modal-title">旅行計画</h2>

            <label className="modal-label">
              出発日
              <input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
              />
            </label>

            {/* 出発時刻追加 */}
            <label className="modal-label">
              出発時刻
              <input
                type="time"
                value={startTime}
                onChange={(e) => setStartTime(e.target.value)}
              />
            </label>

            <label className="modal-label">
              到着日
              <input
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
              />
            </label>

            {/* 到着時刻追加 */}
            <label className="modal-label">
              到着時刻
              <input
                type="time"
                value={endTime}
                onChange={(e) => setEndTime(e.target.value)}
              />
            </label>

            <label className="modal-label">
              出発地点
              <input
                type="text"
                value={departure}
                onChange={(e) => setDeparture(e.target.value)}
                placeholder="例）東京駅"
              />
            </label>

            <label className="modal-label">
              旅行先都道府県
              <select
                value={destination}
                onChange={(e) => setDestination(e.target.value)}
              >
                <option value="">選択してください</option>
                {prefectures.map((group, idx) => (
                  <optgroup key={idx} label={group.label}>
                    {group.options.map((pref) => (
                      <option key={pref} value={pref}>{pref}</option>
                    ))}
                  </optgroup>
                ))}
              </select>
            </label>

            <label className="modal-label">
              ジャンル
              <select
                value={genre}
                onChange={(e) => setGenre(e.target.value)}
              >
                <option value="人気">人気</option>
                <option value="歴史">歴史</option>
                <option value="絶景">絶景</option>
                <option value="レジャー">レジャー</option>
              </select>
            </label>

            <label className="modal-label">
              旅行人数
              <input
                type="number"
                value={peopleCount}
                onChange={(e) => setPeopleCount(e.target.value)}
                placeholder="例）4"
              />
            </label>

            <label className="modal-label">
              予算
              <input
                type="number"
                value={budget}
                onChange={(e) => setBudget(e.target.value)}
                placeholder="例）100000"
              />
            </label>

            <div className="modal-buttons">
              <button className="modal-cancel" onClick={handleCloseModal}>
                キャンセル
              </button>
              <button className="modal-execute" onClick={handleExecute}>
                実行
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ローディング (4秒) */}
      {isLoading && (
        <div className="loading-overlay">
          <div className="loading-message">
            <div className="spinner"></div>
            <p>AIによって選定中...</p>
          </div>
        </div>
      )}
    </main>
  );
}

export default MainPage;
