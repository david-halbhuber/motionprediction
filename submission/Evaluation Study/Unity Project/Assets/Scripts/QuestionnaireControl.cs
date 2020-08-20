using System;
using System.Linq;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Text;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

struct QuestionnaireItem
{
    public int id;
    public string text;
    public string[] answers;

    public QuestionnaireItem(int itemId, string itemText, string[] itemAnswers)
    {
        id = itemId;
        text = itemText;
        answers = itemAnswers;
    }
}

public class QuestionnaireControl : MonoBehaviour
{
    // public properties 
    public TextMeshPro questionText, answerOne, answerTwo, answerThree, answerFour, answerFive;
    public GameObject forwardButton, startQuestionnaireButton;
    public int personId;

    // private properties
    public int currentQuestionIndex;
    private List<QuestionnaireItem> randomizedQuestions = new List<QuestionnaireItem>();
    private ToggleGroup toggleGroup;
    private string filePath = "C:\\Users\\LocalAdmin\\Documents\\Projekte\\VR-Prediction\\questionnaire.csv";

    // IPQ questions
    List<QuestionnaireItem> ipqQuestions = new List<QuestionnaireItem>()
    {
        new QuestionnaireItem( 1, "In der computererzeugten Welt hatte ich den Eindruck, dort gewesen zu sein...", new string[] {"überhaupt nicht", "wenig", "neutral", "stark", "sehr stark"}),
        new QuestionnaireItem( 6, "Ich fühlte mich im virtuellen Raum anwesend.", new string[] {"trifft gar nicht zu", "trifft nicht zu", "neutral", "trifft zu", "trifft voll zu"}),
        new QuestionnaireItem( 10, "Meine Aufmerksamkeit war von der virtuellen Welt völlig in Bann gezogen.", new string[] {"trifft gar nicht zu", "trifft nicht zu", "neutral", "trifft zu", "trifft voll zu"}),
    };

    // latency questions 
    List<QuestionnaireItem> latencyQuestions = new List<QuestionnaireItem>()
    {
        new QuestionnaireItem( 101, "Ich hatte das Gefühl, dass sich mein virtueller Körper an der gleichen Position wie in der Realität befand.", new string[] {"trifft gar nicht zu", "trifft nicht zu", "neutral", "trifft zu", "trifft voll zu"}),
        new QuestionnaireItem( 102, "Ich hatte das Gefühl, dass die Berührung in der Realität durch die Berührung in der virtuellen Welt erzeugt wurde.", new string[] {"trifft gar nicht zu", "trifft nicht zu", "neutral", "trifft zu", "trifft voll zu"}),
        new QuestionnaireItem( 103, "Meine Bewegungen in der virtuellen Realität wurden von mir durchgeführt.", new string[] {"trifft gar nicht zu", "trifft nicht zu", "neutral", "trifft zu", "trifft voll zu"}),
        new QuestionnaireItem( 104, "Es erschien mir, dass mein Körper in die virtuelle Welt platziert wurde.", new string[] {"trifft gar nicht zu", "trifft nicht zu", "neutral", "trifft zu", "trifft voll zu"}),
        new QuestionnaireItem( 105, "Der virtuelle Körper glich meinem wirklichen Körper in Form und Aussehen.", new string[] {"trifft gar nicht zu", "trifft nicht zu", "neutral", "trifft zu", "trifft voll zu"}),
        new QuestionnaireItem( 106, "Meine Gefühle wurden durch das Gesehene in der virtuellen Realität beeinflusst.", new string[] {"trifft gar nicht zu", "trifft nicht zu", "neutral", "trifft zu", "trifft voll zu"}),
        new QuestionnaireItem( 107, "Mein virtueller Körper fühlte sich wie mein richtiger Körper an.", new string[] {"trifft gar nicht zu", "trifft nicht zu", "neutral", "trifft zu", "trifft voll zu"})
    };

    public void Start()
    {
        toggleGroup = GetComponent<ToggleGroup>();

        gameObject.SetActive(false);
    }

    // generate and show questionnaire
    public void StartQuestionnaire()
    {
        Debug.Log("Starting questionnaire...");

        startQuestionnaireButton.SetActive(false);
        gameObject.SetActive(true);
        forwardButton.SetActive(false);
        
        currentQuestionIndex = 0;
        randomizedQuestions.Clear();
        
        foreach (QuestionnaireItem qi in ShuffleList(ipqQuestions))
        {
            randomizedQuestions.Add(qi);
        }
        foreach (QuestionnaireItem qi in ShuffleList(latencyQuestions))
        {
            randomizedQuestions.Add(qi);
        }
       
        LoadQuestion(currentQuestionIndex);
    }

    // hide questionnaire 
    private void EndQuestionnaire()
    {
        Debug.Log("Ending questionnaire...");
        gameObject.SetActive(false);
        startQuestionnaireButton.SetActive(false);
    }

    public void SaveAndNextQuestion()
    {
        SaveAnswer();
        if (currentQuestionIndex + 1 < randomizedQuestions.Count)
        {
            currentQuestionIndex += 1;
            LoadQuestion(currentQuestionIndex);
        }
        else
        {
            EndQuestionnaire();
        }
    }

    // load question
    private void LoadQuestion(int questionIndex)
    {
        Debug.Log("Loading question on index " + questionIndex);
        QuestionnaireItem question = randomizedQuestions[questionIndex];
        questionText.text = question.text;
        answerOne.text = question.answers[0];
        answerTwo.text = question.answers[1];
        answerThree.text = question.answers[2];
        answerFour.text = question.answers[3];
        answerFive.text = question.answers[4];
    }

    // save answer to csv file (format: PersonID, QuestionID, AnswerId, CreatedAt)
    private void SaveAnswer()
    {
        StringBuilder csv = new StringBuilder();
        string timestamp = DateTime.Now.ToString("yyyyMMddHHmmss");
        QuestionnaireItem question = randomizedQuestions[currentQuestionIndex];
        int selectedAnswerId = 0;
        foreach (Toggle toggle in toggleGroup.ActiveToggles())
        {
            toggle.isOn = false;
            selectedAnswerId = toggle.gameObject.GetComponent<AnswerControl>().optionId;
        }
        Debug.Log($"Saving answer: {personId}, {question.id}, {selectedAnswerId}, {timestamp}");
        csv.AppendLine($"{personId},{question.id},{selectedAnswerId},{timestamp}");
        File.AppendAllText(filePath, csv.ToString());
    }


    // randomize list
    private List<QuestionnaireItem> ShuffleList(List<QuestionnaireItem> inputList)
    {
        List<QuestionnaireItem> duplicatedList = new List<QuestionnaireItem>();
        foreach(QuestionnaireItem qi in inputList)
        {
            duplicatedList.Add(qi);
        }
        List<QuestionnaireItem> randomList = new List<QuestionnaireItem>();
        System.Random r = new System.Random();
        while (duplicatedList.Count > 0)
        {
            var randomIndex = r.Next(0, duplicatedList.Count);
            randomList.Add(duplicatedList[randomIndex]);
            duplicatedList.RemoveAt(randomIndex);
        }
        return randomList;
    }
}
