var anchorx = 1;  // 坐标x
var anchory = 1;  // 坐标y
var anchorc = 1;  // 单词坐标
var wordCount = 0;
if (document.getElementById("nextBtn")) {
    document.getElementById("nextBtn").hidden = true;  // 显示下一页面按钮
}
if (document.getElementById("wordCount")) {
    wordCount = Number(document.getElementById("wordCount").innerText);
}
var isAllFinish = false;  // 检测最后一个单词是否完成
// 键盘事件响应
document.onkeydown = function(event){
    var ev = event || window.event;
    var evKeyCode = ev.keyCode;
    // document.getElementById("test").innerHTML = anchorc;
    // 如果输入方向键
    // if (evKeyCode == 37 || evKeyCode == 38 || evKeyCode == 39 || evKeyCode == 40) {
    //     SelectWord(ev);
    // }
    // else {
    //     ChangeWord(ev);
    // }
    ChangeWord(ev);
}
function ChangeWord(ev){
    if (isAllFinish) {
        return
    }
    var evKeyCode = ev.keyCode;
    var selectedLetter = document.getElementById("W" + anchorx + anchory + "C" + anchorc);
    if (selectedLetter) {
        // document.write("a".charCodeAt());
        // 对比新输入的字母与目前选中字母是否相同
        var inputLetter1 = String.fromCharCode(evKeyCode + 32);
         var inputLetter2 = String.fromCharCode(evKeyCode);
        var targetLetter = selectedLetter.innerText;
        // 如果输入符合条件，添加相应类名
        if (targetLetter == inputLetter1 || targetLetter == inputLetter2) {
            selectedLetter.className = "inputTrue";
            //// 自动选择下个单词
            var isFinish = document.getElementById("W" + anchorx + anchory).getAttribute("data-finish");
            if (isFinish != "true") {
                if (selectedLetter.getAttribute("data-last") == "true") {
                    document.getElementById("W" + anchorx + anchory).dataset.finish = "true";
                    anchory += 1;
                    var isLast = document.getElementById("W" + anchorx + (anchory-1)).getAttribute("data-last");
                    if (isLast != "true") {
                        document.getElementsByClassName("selectWord")[0].classList.remove("selectWord");
                        document.getElementById("W" + anchorx + anchory).className += " selectWord";  // 把选中单词赋予类
                    }
                    else {
                        isAllFinish = true;  // 全部结束
                        if (document.getElementById("nextBtn")) {
                            document.getElementById("nextBtn").hidden = false;  // 显示下一页面按钮
                        }
                    }
                    anchorc = 1;  // 字母锚点初始化
                    return
                }
            }
            ////
            anchorc += 1;  // 锚点移一位
        }
    }
    else
    {
        return
    }
}
// 选择响应
function SelectWord(ev){
    var evKeyCode = ev.keyCode;
    // 取出当前单词是否输入完成标志
    var isFinish = document.getElementById("W" + anchorx + anchory).getAttribute("data-finish");
    // 把超出界限的锚点移回最后一位字母
    anchorc -= 1;
    if (isFinish != "true") {
        var selectedLetter = document.getElementById("W" + anchorx + anchory + "C" + anchorc);
        if (selectedLetter) {
            if (selectedLetter.getAttribute("data-last") == "true" && selectedLetter.className == "inputTrue") {
                document.getElementById("W" + anchorx + anchory).dataset.finish = "true";
            }
            else {
                for (var i = 0; i < anchorc; i++) {
                    document.getElementById("W" + anchorx + anchory + "C" + (i+1)).className = "";
                }
            }
        }
    }
    if (evKeyCode == 37) {
        if (anchory > 1) {
            anchory -= 1;  // 选择左
        }
    }
    else if (evKeyCode == 38) {
        if (anchory > 2) {
            anchory -= 2;  // 选择上
        }
    }
    else if (evKeyCode == 39) {
        if (anchory < wordCount) {
            anchory += 1;  // 选择右
        }
    }
    else if (evKeyCode == 40) {
        if (anchory < wordCount-1) {
            anchory += 2;  // 选择下
        }
    }
    // document.getElementsByClassName("selectWord")[0].className = "";  // 清空选中类别
    document.getElementsByClassName("selectWord")[0].classList.remove("selectWord");
    document.getElementById("W" + anchorx + anchory).className += " selectWord";  // 把选中单词赋予类
    anchorc = 1;  // 字母锚点初始化
}
function Init(){
    document.getElementById("W11").className += " selectWord";
}
// 页面加载
window.onload = function(){
    Init();  // 初始化
}
