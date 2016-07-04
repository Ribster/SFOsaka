#include "SFOTranslateController.h"

#include "SFOContext.h"

#include <QDebug>
#include <QQmlContext>
#include <QStringListModel>

#include <iostream>

const QString SFOTranslateController::ControllerIdentifier = "translateController";
const QString SFOTranslateController::ModelIdentifier = "translationModel";

SFOTranslateController::SFOTranslateController(QQmlContext *context,
                                               QObject *parent) :
    QObject(parent),
    _context(context)
{
    _context->setContextProperty(ControllerIdentifier, this);
    _context->setContextProperty(ModelIdentifier, QVariant());

    SFOContext* ctx = SFOContext::GetInstance();
    // Listen for the partners updated signal so we can updated ourselves
    QObject::connect(ctx, &SFOContext::DictionariesUpdated,
                     this, &SFOTranslateController::_HandleDictionariesUpdate);

}

SFOTranslateController::~SFOTranslateController()
{
    // nothing now
}

void
SFOTranslateController::OnInputAccepted(const QString& text)
{
    qDebug() << "[" << text << "]";
    // Gets the first character to see if we're in Japanese or English.
    InputLanguage lang = _GetInputLanguage(text);
    if (lang == InvalidInput)
        return;

    QString lowered = text.toLower();
    QStringList translations;
    SFOContext *context = SFOContext::GetInstance();
    if (lang == JapaneseInput) {
        translations = _GetMatch(lowered, context->GetJpToEnDict());
    } else if (lang == EnglishInput) {
        translations = _GetMatch(lowered, context->GetEnToJpDict());
    }

    qDebug() << "translations: " << translations;
    QStringList* list = new QStringList(translations);
    _translatedText = QStringListSharedPtr(list);
    _context->setContextProperty(ModelIdentifier,
                                 QVariant::fromValue(*list));
}

void
SFOTranslateController::_HandleDictionariesUpdate()
{
    qDebug() << "Dictionary updtaed from server";
}

SFOTranslateController::InputLanguage
SFOTranslateController::_GetInputLanguage(const QString& input) const
{
    if (input.length() == 0)
        return InvalidInput;

    QChar inputChar = input.at(0);
    switch (inputChar.script()) {
    case QChar::Script_Latin:
        return EnglishInput;
    case QChar::Script_Hiragana:
    case QChar::Script_Katakana:
    case QChar::Script_Han:
        return JapaneseInput;
    default:
        return InvalidInput;
    }

}

QStringList
SFOTranslateController::_GetMatch(const QString& str,
                                  const QStringMap& dict) const
{
    QStringList matches;
    for (QStringMap::const_iterator mit = dict.constBegin() ;
         mit != dict.constEnd() ; ++mit) {
        qDebug() << str << " to " << mit.key();
        if (mit.key().contains(str)) {
            matches.append(mit.key() + ": " + mit.value());
        }
    }

    return matches;
}