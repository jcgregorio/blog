import selector 
import view

urls = selector.Selector()

urls.add('/cookbook/json/[{id}][;{noun}]', _ANY_=view.JSONCollection())
urls.add('/cookbook/', GET=view.list)

