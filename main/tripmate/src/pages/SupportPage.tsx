import React from 'react';
import './SupportPage.css';

function SupportPage() {
  const handleContact = () => {
    alert('お問い合わせが送信されました。');
  };

  return (
    <div className="support-container">
      <h2>サポート</h2>
      <p>何かお困りのことがありましたら、以下のフォームからお問い合わせください。</p>
      <div className="support-form">
        <label>
          お問い合わせ内容:
          <textarea rows={5} />
        </label>
        <button onClick={handleContact}>送信</button>
      </div>
    </div>
  );
}

export default SupportPage;
