var anchorx = 1;  // 坐标x
var anchory = 1;  // 坐标y
var anchorc = 1;  // 单词坐标
var wordCount = 0;
var finish_count = 0;  // 单词完成次数
var count_index = 0;  // 控制动画的索引
var deviation_list = [];  // 单词偏差值列表
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
            selectedLetter.className += " inputTrue";
            if (finish_count == 2) {
                selectedLetter.style.color = "";
                selectedLetter.style.backgroundColor = "";
            }
            //// 自动选择下个单词
            var isFinish = document.getElementById("W" + anchorx + anchory).getAttribute("data-finish");
            if (isFinish != "true") {
                count_index = anchory;
                if (selectedLetter.getAttribute("data-last") == "true") {
                    document.getElementById("finishCount" + anchory).style.fontSize = "26px";
                    // 完成第一次
                    if (finish_count == 0) {
                        finish_count += 1;
                        document.getElementById("finishCount" + anchory).innerHTML = finish_count;
                        var letter_list = document.getElementsByClassName("letter" + anchory);
                        for (var j = 0,len = letter_list.length; j < len; j++) {
                            letter_list[j].classList.remove("inputTrue"); 
                        }
                    }  // 完成第二次
                    else if (finish_count == 1) {
                        finish_count += 1;
                        document.getElementById("finishCount" + anchory).innerHTML = finish_count;
                        var letter_list = document.getElementsByClassName("letter" + anchory);
                        for (var j = 0,len = letter_list.length; j < len; j++) {
                            letter_list[j].classList.remove("inputTrue"); 
                            letter_list[j].style.color = "#fff";
                            letter_list[j].style.backgroundColor = "#fff";
                        }
                    }  // 完成第三次
                    else {
                        finish_count = 0;
                        document.getElementById("finishCount" + anchory).innerHTML = 3;
                        document.getElementById("W" + anchorx + anchory).dataset.finish = "true";
                        anchory += 1;
                        // document.getElementById("deviation_list").value = deviation_list;  // 提交偏差值列表  // 测试位置
                        var isLast = document.getElementById("W" + anchorx + (anchory-1)).getAttribute("data-last");
                        if (isLast != "true") {
                            document.getElementsByClassName("selectWord")[0].classList.remove("selectWord");  // 去掉某一类
                            document.getElementById("W" + anchorx + anchory).className += " selectWord";  // 把选中单词赋予类
                        }
                        else {
                            isAllFinish = true;  // 全部结束
                            document.getElementById("deviation_list").value = deviation_list;  // 提交偏差值列表  // 真正位置
                            if (document.getElementById("nextBtn")) {
                                document.getElementById("nextBtn").hidden = false;  // 显示下一页面按钮
                            }
                        }
                    }
                    setTimeout('document.getElementById("finishCount" + count_index).style.fontSize = "16px";', 300);
                    anchorc = 1;  // 字母锚点初始化
                    return
                }
            }
            ////
            anchorc += 1;  // 锚点移一位
        }
        else {
            if (finish_count == 2 && anchorc != 1) {
                var letter_list = document.getElementsByClassName("letter" + anchory);
                for (var j = 0, len = letter_list.length; j < len; j++) {
                    letter_list[j].classList.remove("inputTrue"); 
                    letter_list[j].style.color = "#fff";
                    letter_list[j].style.backgroundColor = "#fff";
                }
                if (deviation_list[anchory - 1] == 10 || deviation_list[anchory - 1] == -5) {
                    deviation_list[anchory - 1] -= 5;
                }
                else if (deviation_list[anchory - 1] == 5) {
                    deviation_list[anchory - 1] = -5;
                }
                anchorc = 1;  // 字母锚点初始化
            } 
        } 
    }
    else
    {
        return
    }
}
// 初始化函数
function Init(){
    document.getElementById("W11").className += " selectWord";
    for (var i = 0; i < wordCount; i++) {
        deviation_list.push(10);
    }
    // document.getElementById("deviation_list").value = deviation_list;  // 测试位置
}
// 页面加载
window.onload = function(){
    Init();  // 初始化
}
