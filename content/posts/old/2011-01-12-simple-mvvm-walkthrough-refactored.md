---
title: Simple MVVM Walkthrough – Refactored
slug: simple-mvvm-walkthrough-refactored
date: '2011-01-12T07:07:00'
updated: '2011-01-12T07:07:00'
draft: false
author: Sean Feldman
---


JR has put together a good [introduction post](http://agilewarrior.wordpress.com/2011/01/11/simple-mvvm-walkthrough-part-i/) into MVVM pattern. I love kick start examples that serve the purpose well. And even more than that I love examples that also can pass the real world projects check. So I took the sample code and refactored it slightly for a few aspects that a lot of developers might raise a eyebrow.

Michael [has mentioned](http://agilewarrior.wordpress.com/2011/01/11/simple-mvvm-walkthrough-part-i/#comment-515) model (entity) visibility from view. I agree on that. A few other items that don’t settle are using property names as string (magical strings) and Saver class internal casting of a parameter (custom code for each Saver command).

Fixing a property names usage is a straight forward exercise – leverage expressions. Something simple like this would do the initial job:

```
class PropertyOf<T>  
  {  
    public static string Resolve(Expression<Func<T, object>> expression)  
    {  
      var member = expression.Body as MemberExpression;  
      return member.Member.Name;  
    }  
  }
```

With this, refactoring property names becomes an easy task, with confidence that an old property name will not stay in the code after property gets renamed. An updated Invoice would look like this:

```
public class Invoice : INotifyPropertyChanged  
  {  
    private int id;  
    private string receiver;  
  
    public event PropertyChangedEventHandler PropertyChanged;  
  
    private void OnPropertyChanged(string propertyName)  
    {  
      if (PropertyChanged != null)  
      {  
        PropertyChanged(this, new PropertyChangedEventArgs(propertyName));  
      }  
    }  
  
    public int Id  
    {  
      get { return id; }  
      set  
      {  
        if (id != value)  
        {  
          id = value;  
          OnPropertyChanged(PropertyOf<Invoice>.Resolve(x => x.Id));  
        }  
      }  
    }  
  
    public string Receiver  
    {  
      get { return receiver; }  
      set  
      {  
        receiver = value;  
        OnPropertyChanged(PropertyOf<Invoice>.Resolve(x => x.Receiver));  
      }  
    }  
  }
```

For the saver, I decided to change it a little so now it becomes a “view-model agnostic” command, one that can be used for multiple commands/view-models. Reason for this is the fact that on average UI has more than a single command. Updated Saver now accepts an action at the construction time and executes that action when command is exercised. No more black magic ![Smile](http://weblogs.asp.net/blogs/sfeldman/wlEmoticon-smile_5E0AE80F.png)

```
  internal class Command : ICommand  
  {  
    private readonly Action executeAction;  
  
    public Command(Action executeAction)  
    {  
      this.executeAction = executeAction;  
    }  
  
    public bool CanExecute(object parameter)  
    {  
      return true;  
    }  
  
    public event EventHandler CanExecuteChanged;  
  
    public void Execute(object parameter)  
    {  
      // no more black magic  
      executeAction();  
    }  
  }
```

Change in InvoiceViewModel is instantiation of Saver command and execution action for the specific command.

```
 public ICommand SaveCommand  
    {  
      get  
      {  
        if (saveCommand == null)  
          saveCommand = new Command(ExecuteAction);  
        return saveCommand;  
      }  
      set { saveCommand = value; }  
    }  
  
    private void ExecuteAction()  
    {  
      DisplayMessage = string.Format("Thanks for creating invoice: {0} {1}", Invoice.Id, Invoice.Receiver);  
    }
```

This way internal knowledge of InvoiceViewModel remains in InvoiceViewModel and Command (ex-Saver) is view-model agnostic.

Now the sample is not only a good introduction, but also has some practicality in it. My 5 cents on the subject.

Sample code [MvvmSimple2.zip](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/MvvmSimple2_435C5566.zip)

Update 2011-01-12: I have addressed the null exception issue in [part 2](/sfeldman/archive/2011/01/12/simple-mvvm-walkthrough-refactored-part-2.aspx).   



