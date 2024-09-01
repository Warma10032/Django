from enum  import Enum

class userPurposeType(Enum):
    #根据用户输入的文本信息的可能问题类型预定义
    Unknown= 0  #未知问题
    Voice = 1   #语音生成
    Audio = 2   #视频生成
    ImageGeneration = 3 #文生图
    ImageDescride = 4 #图生文
    Ducument = 5  #基于文件描述，后面有个向量库，对于单个用户，尽量从向量数据库给出回答，可能涉及检索加强
    Hello = 6   #问候语，给出特定输出

    
purpose_map={
"其他":userPurposeType.Unknown,
"语音生成":userPurposeType.Voice,
"视频生成":userPurposeType.Audio,
"图片描述":userPurposeType.ImageDescride,
"图片生成":userPurposeType.ImageGeneration,
"基于文件描述":userPurposeType.Ducument,
"问候语":userPurposeType.Hello,
}

