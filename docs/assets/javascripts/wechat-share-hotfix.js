/* WeChat share hotfix:
 * Copy current page URL to clipboard when user clicks "发送给朋友".
 */
(function () {
  function disableFooterHoverTooltip() {
    var links = document.querySelectorAll(".md-footer__link[aria-label]");
    links.forEach(function (link) {
      link.removeAttribute("aria-label");
    });
  }

  function fallbackCopy(text) {
    var textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.setAttribute("readonly", "");
    textarea.style.position = "absolute";
    textarea.style.left = "-9999px";
    document.body.appendChild(textarea);
    textarea.select();
    var ok = document.execCommand("copy");
    document.body.removeChild(textarea);
    if (!ok) {
      throw new Error("execCommand copy failed");
    }
  }

  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text).catch(function () {
        fallbackCopy(text);
      });
    }

    try {
      fallbackCopy(text);
      return Promise.resolve();
    } catch (err) {
      return Promise.reject(err);
    }
  }

  window.shareToWechat = function (event) {
    if (event) {
      event.preventDefault();
      event.stopPropagation();
    }

    var pageUrl = window.location.href;
    return copyText(pageUrl)
      .then(function () {
        alert("页面链接已复制到剪贴板，请粘贴发送给微信好友。");
        return false;
      })
      .catch(function () {
        alert("复制失败，请手动复制当前页面链接后发送给微信好友。");
        return false;
      });
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", disableFooterHoverTooltip);
  } else {
    disableFooterHoverTooltip();
  }

  // Keep single trigger path to avoid duplicate alerts:
  // button uses inline onclick="return shareToWechat(event);"
})();
