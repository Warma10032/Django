from enum  import Enum

class userPurposeType(Enum):
    #根据用户输入的文本信息的可能问题类型预定义
    Unknown= 0  #未知问题
    Text = 1    #普通文本问题
    Voice = 2   #语音生成
    Audio = 3   #视频生成
    ImageGeneration = 4 #文生图
    ImageDescride = 5 #图生文
    Ducument = 6  #基于文件描述，后面有个向量库，对于单个用户，尽量从向量数据库给出回答，可能涉及检索加强
    Hello = 7    #问候语，给出特定输出

    
purpose_map={
"其他":userPurposeType.Unknown,
"文本生成":userPurposeType.Text,
"语音生成":userPurposeType.Voice,
"视频生成":userPurposeType.Audio,
"图片描述":userPurposeType.ImageGeneration,
"图片生成":userPurposeType.ImageDescride,
"基于文件描述":userPurposeType.Ducument,
"问候语":userPurposeType.Hello,
}

