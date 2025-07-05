import React, { useState } from "react";
import "./Select.css";

interface Attraction {
  name: string;
  address: string;
  time: string;   // e.g. "1時間", "50分"
  cost: string;   // e.g. "200円"
  image: string;  // 画像パス
  popularity?: number; // ソート用(人気順)
}

const initialAttractions: Attraction[] = [
  { name: "五色沼", address: "福島県会津若松", time: "1時間", cost: "0円", image: "/assets/goshikinuma.jpg", popularity: 2 },
  { name: "鶴ヶ城", address: "福島県会津若松", time: "1.5時間", cost: "210円", image: "/assets/tsurugajo.jpg", popularity: 0 },
  { name: "高湯温泉", address: "福島県福島市", time: "1時間", cost: "1000円", image: "/assets/takayu.jpg", popularity: 12 },
  { name: "まるえ観光果樹園", address: "福島県福島市", time: "50分", cost: "1210円", image: "/assets/marue.jpg", popularity: 11 },
  { name: "あぶくま洞", address: "福島県田村市", time: "1.5時間", cost: "1200円", image: "/assets/abukumado.jpg", popularity: 6 },
  { name: "スパリゾートハワイアンズ", address: "福島県いわき市", time: "3時間", cost: "3570円", image: "/assets/hawai.jpg", popularity: 3 },
  { name: "塔のへつり", address: "福島県南会津郡", time: "1時間", cost: "0円", image: "/assets/tounoheturi.jpg", popularity: 9 },
  { name: "会津さざえ堂", address: "福島県会津若松", time: "40分", cost: "600円", image: "/assets/sazaedou.jpg", popularity: 7 },
  { name: "大内宿", address: "福島県南会津郡", time: "2.5時間", cost: "3000円", image: "/assets/ouchijuku.jpg", popularity: 4 },
  { name: "アクアマリン福島", address: "福島県いわき市", time: "2時間", cost: "1850円", image: "/assets/akuamarin.jpg", popularity: 1 },
  { name: "花見山公園", address: "福島県福島市", time: "30分", cost: "0円", image: "/assets/hanamiyama.jpg", popularity: 8 },
  { name: "野口英世記念館", address: "福島県耶麻郡", time: "40分", cost: "1200円", image: "/assets/noguti.jpg", popularity: 10 },
  { name: "郡山布引風の高原", address: "福島県郡山市", time: "30分", cost: "0円", image: "/assets/himawari.jpg", popularity: 5 },
];

// ソート用のパース関数
function parseCost(costStr: string): number {
  return Number(costStr.replace('円', ''));
}
function parseTime(timeStr: string): number {
  if (timeStr.includes('時間')) {
    return Number(timeStr.replace('時間',''));
  } else if (timeStr.includes('分')) {
    const min = Number(timeStr.replace('分',''));
    return min / 60;
  }
  return 1;
}

const Select: React.FC = () => {
  // 全観光地(ソート・ページング用)
  const [allAttractions, setAllAttractions] = useState<Attraction[]>([...initialAttractions]);
  
  // ページング (6件表示)
  const [pageIndex, setPageIndex] = useState(0);
  const ITEMS_PER_PAGE = 6;
  const start = pageIndex * ITEMS_PER_PAGE;
  const end = start + ITEMS_PER_PAGE;
  const displayed = allAttractions.slice(start, end);

  // 選択管理
  const [selectedAttractions, setSelectedAttractions] = useState<Attraction[]>([]);
  const [selectedIds, setSelectedIds] = useState<number[]>([]);

  // しおり作成(ロード)
  const [isCreating, setIsCreating] = useState(false);
  const [showRedirectMsg, setShowRedirectMsg] = useState(false);

  // 最後に押したソートボタン (人気,費用,時間)
  const [lastSort, setLastSort] = useState<'popularity' | 'cost' | 'time' | ''>('');

  // 選択/解除
  const handleAttractionClick = (index: number) => {
    const realIndex = start + index;
    if (selectedIds.includes(realIndex)) {
      // 解除
      setSelectedIds((prev) => prev.filter((id) => id !== realIndex));
      setSelectedAttractions((prev) =>
        prev.filter((attr) => attr.name !== allAttractions[realIndex].name)
      );
    } else {
      // 追加
      setSelectedIds((prev) => [...prev, realIndex]);
      setSelectedAttractions((prev) => [...prev, allAttractions[realIndex]]);
    }
  };

  // ページ移動
  const handlePreviousProposal = () => {
    if (pageIndex > 0) {
      setPageIndex(pageIndex - 1);
    } else {
      alert('これ以上前の提案はありません');
    }
  };
  const handleNextProposal = () => {
    if (end < allAttractions.length) {
      setPageIndex(pageIndex + 1);
    } else {
      alert('これ以上の提案はありません');
    }
  };

  // ソート処理
  const handleSortPopularity = () => {
    const newList = [...allAttractions].sort((a,b) => (a.popularity ?? 0) - (b.popularity ?? 0));
    setAllAttractions(newList);
    setPageIndex(0);
    setLastSort('popularity');
  };
  const handleSortCost = () => {
    const newList = [...allAttractions].sort((a,b) => parseCost(a.cost) - parseCost(b.cost));
    setAllAttractions(newList);
    setPageIndex(0);
    setLastSort('cost');
  };
  const handleSortTime = () => {
    const newList = [...allAttractions].sort((a,b) => parseTime(a.time) - parseTime(b.time));
    setAllAttractions(newList);
    setPageIndex(0);
    setLastSort('time');
  };

  // しおり作成 (4秒 -> 1秒後にマップ画面に移動)
  const handleCreateShiori = () => {
    setIsCreating(true);
    setTimeout(() => {
      setIsCreating(false);
      setShowRedirectMsg(true);
      setTimeout(() => {
        // 本番環境では /api、開発環境では localhost:3001 に遷移
        const isProduction = process.env.NODE_ENV === 'production';
        const mapUrl = isProduction ? '/api' : 'http://localhost:3001';
        window.open(mapUrl, '_blank');
      }, 1000);
    }, 4000);
  };

  // 選択観光地の合計費用 (数値化して合計)
  const totalCost = selectedAttractions.reduce((acc, item) => {
    return acc + parseCost(item.cost);
  }, 0);

  return (
    <main className="select-container">
      {/* ソートボタン */}
      <div className="sort-buttons">
        <button
          onClick={handleSortPopularity}
          className={lastSort === 'popularity' ? 'active-sort' : ''}
        >
          人気順
        </button>
        <button
          onClick={handleSortCost}
          className={lastSort === 'cost' ? 'active-sort' : ''}
        >
          費用順
        </button>
        <button
          onClick={handleSortTime}
          className={lastSort === 'time' ? 'active-sort' : ''}
        >
          所要時間順
        </button>
      </div>

      {/* 観光地カード */}
      <div className="attraction-grid">
        {displayed.map((attraction, index) => {
          const realIndex = start + index;
          const selected = selectedIds.includes(realIndex);
          return (
            <div
              className={`attraction-card ${selected ? "selected" : ""}`}
              key={realIndex}
              onClick={() => handleAttractionClick(index)}
            >
              <img
                src={attraction.image}
                alt={attraction.name}
                className="attraction-image"
              />
              <div className="attraction-info">
                <h3 className="attraction-name">{attraction.name}</h3>
                <p>住所: {attraction.address}</p>
                <p>所要時間: {attraction.time}</p>
                <p>費用: {attraction.cost}</p>
              </div>
            </div>
          );
        })}
      </div>

      <div className="proposal-button-container">
        <button onClick={handlePreviousProposal}>前の提案先</button>
        <span className="page-number">ページ {pageIndex + 1}</span>
        <button onClick={handleNextProposal}>次の提案先</button>
      </div>

      {/* 選択済み一覧 */}
      <div className="selection-list">
        <h3>選択済み一覧</h3>
        <ul>
          {selectedAttractions.map((attr, i) => (
            <li key={i}>
              {attr.name} - {attr.address} - {attr.cost} - {attr.time}
            </li>
          ))}
        </ul>
        {/* 合計費用 & 選択個数 */}
        <div className="selected-summary">
          <p>選択個数: {selectedAttractions.length} 件</p>
          <p>合計費用: {totalCost} 円</p>
        </div>
      </div>

      {/* しおり作成ボタン */}
      <div className="bookmark-button-container">
        <button className="bookmark-button" onClick={handleCreateShiori}>
          しおり作成
        </button>
      </div>

      {/* しおり作成中 */}
      {isCreating && (
        <div className="creating-overlay">
          <div className="creating-message">
            <div className="spinner"></div>
            <p>AIしおり作成中...</p>
          </div>
        </div>
      )}

      {/* 遷移メッセージ */}
      {showRedirectMsg && (
        <div className="redirect-msg">
          <p>別ページに遷移します</p>
        </div>
      )}
    </main>
  );
};

export default Select;
