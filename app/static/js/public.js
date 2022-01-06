/*
 * @Date: 2021-12-09 12:30:39
 * @LastEditTime: 2021-12-12 23:55:49
 * @Description: file content
 */
(function (params) {
  window.message = function (type, message) {
    window.ELEMENT.Message({
      message,
      type,
    });
  };
  window.sleep = function (time) {
    return new Promise((resolve) => setTimeout(resolve, time * 1000));
  };
  window.request = function (type, url, data) {
    return new Promise((resolve, reject) => {
      $.ajax({
        type,
        url,
        timeout: 6 * 60 * 1000,
        data: type === "POST" ? JSON.stringify(data) : undefined,
        dataType: "json",
        contentType: "application/json",
        success: function (res) {
          console.log(res);
          if (res.code) {
            reject(res);
            return;
          }
          resolve(res);
        },
        error: function (res) {
          reject(res);
        },
      });
    });
  };
})();
