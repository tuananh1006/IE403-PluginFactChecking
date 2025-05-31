document.addEventListener("DOMContentLoaded", () => {
    const resultBox = document.getElementById("resultDisplay");
  
    document.getElementById("checkClaimInput").addEventListener("click", async () => {
      const model = document.getElementById("aiModel").value;
      const claim = document.getElementById("claimInput").value.trim();
  
      if (!claim) {
        resultBox.textContent = "⚠️ Vui lòng nhập thông tin cần kiểm chứng.";
        return;
      }
  
      resultBox.textContent = `🔍 Đang kiểm chứng thông tin bằng mô hình ${model}...`;
  
      // 👉 Giả lập dữ liệu bằng chứng
      const evidences = [
        {
          source: "https://vnexpress.net/de-xuat-tp-hcm-bo-cap-giay-phep-xay-dung-tu-1-7-4892783.html",
          content: "Người đứng đầu chính phủ cũng yêu cầu Bộ Xây dựng phải rút gọn thủ tục cấp phép xây dựng với dự án đã có quy hoạch chi tiết 1/500 hoặc nằm trong khu vực có thiết kế đô thị. Chỉ đạo lần này được xem là bước đi mạnh mẽ nhằm tháo gỡ điểm nghẽn thủ tục trong lĩnh vực xây dựng - một trong những rào cản lớn với quá trình phục hồi và phát triển của thị trường bất động sản cũng như các dự án hạ tầng trên cả nước",
          label: "SUPPORTS"
        },
        {
          source: "https://video.vnexpress.net/tiem-kich-cuong-kich-huan-luyen-nem-bom-4892247.html",
          content: "Su-30MK2, Su-27, Su-22, Yak-130 phô diễn sức mạnh ném bom chính xác tại trung tâm huấn luyện Quốc gia TB2 ở Bình Định.",
          label: "REFUTES"
        }
      ];
  
      resultBox.textContent = `✅ Kết quả kiểm chứng bởi ${model}`;
      renderEvidenceTabs(evidences);
    });
  
    document.getElementById("btnSupport").addEventListener("click", () => {
      showEvidence("SUPPORTS");
    });
  
    document.getElementById("btnRefute").addEventListener("click", () => {
      showEvidence("REFUTES");
    });
  });
  
  let allEvidences = [];
  
  function renderEvidenceTabs(evidences) {
    const supportCount = evidences.filter(e => e.label === "SUPPORTS").length;
    const refuteCount = evidences.filter(e => e.label === "REFUTES").length;
  
    document.getElementById("countSupport").textContent = supportCount;
    document.getElementById("countRefute").textContent = refuteCount;
  
    allEvidences = evidences;
    document.getElementById("evidenceNav").style.display = "flex";
  
    showEvidence("SUPPORTS");
  }
  
  function showEvidence(label) {
    const list = document.getElementById("evidenceList");
    list.innerHTML = "";
  
    const filtered = allEvidences.filter(e => e.label === label);
  
    filtered.forEach((evi, i) => {
      list.innerHTML += `
        <div class="evidence-item">
          <div>
            <em>Nguồn:</em>
            <a href="#" class="open-source-link" data-source="${evi.source}" data-text="${evi.content}">
              ${new URL(evi.source).hostname}
            </a><br>
            <em>Thông tin liên quan:</em>
            <p>${evi.content}</p>
          </div>
        </div>
        <hr>
      `;
    });
  
    list.style.display = "block";
  
    // Gán sự kiện cho từng link
    document.querySelectorAll(".open-source-link").forEach(link => {
        link.addEventListener("click", (e) => {
          e.preventDefault();
          const url = link.dataset.source;
          const text = link.dataset.text;
      
          chrome.tabs.update({ url: url }, () => {
            // Lấy tab hiện tại sau khi đã cập nhật URL
            chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
              const updatedTab = tabs[0];
              const tabId = updatedTab.id;
          
              // Đợi trang load xong một chút rồi inject + gửi message
              setTimeout(() => {
                chrome.scripting.executeScript({
                  target: { tabId: tabId },
                  files: ["content.js"]
                }, () => {
                  chrome.tabs.sendMessage(tabId, {
                    action: "scrollToText",
                    text: text
                  });
                });
              }, 1000); // có thể tăng lên nếu trang load chậm
            });
          });
          
        });
      });
      
  }
  